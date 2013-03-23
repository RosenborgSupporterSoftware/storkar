#!/usr/bin/env perl

%player = ();

$player{'-'} = '-';
$player{'Alas'} = 'Jaime Alas';
$player{'Bille'} = 'Nicki Bille Nielsen';
$player{'Bråthen'} = 'Erik Mellevold Bråthen';
$player{'Chibbe'} = 'John Chibuike';
$player{'Dockal'} = 'Bořek Dočkal';
$player{'Dorsin'} = 'Micke Dorsin';
$player{'Fredrik'} = 'Fredrik Midtsjø';
$player{'Gamboa'} = 'Cristian Gamboa';
$player{'Jensen'} = 'Mike Jensen';
$player{'Lunna'} = 'Alexander Lund Hansen';
$player{'Mikkelsen'} = 'Tobias Mikkelsen';
$player{'Mix'} = 'Mix';
$player{'Perry'} = 'Per Joar Hansen';
$player{'Reginiussen'} = 'Tore Reginiussen';
$player{'Rønning'} = 'Per Verner Rønning';
$player{'Selnæs'} = 'Ole Kristian Selnæs';
$player{'Svensson'} = 'Jonas Svensson';
$player{'Tarik'} = 'Tarik Elyounoussi';
$player{'Ørlund'} = 'Daniel Örlund';

%winner = ();

$game = "";
$home = 1;

%guess = ();
%pause = ();
%goals = ();

$forlengs = 0;
$baklengs = 0;
$counter = 0;

%score = ();
%scores = ();
$scorescount = 0;
%ranking = ();
  

$linenum = 0;

$round = 0;

sub WriteTable {
  $tablefile = "resultattips-$round.bb";
  print "Writing BBCode to '$tablefile'\n";

  open(BBCODE, ">$tablefile") || die "could not open '$tablefile' for writing.";

  print BBCODE "<center>";
  print BBCODE "<table border=\"2\" bordercolor=\"black\">";
  # print BBCODE "\n";

  $fulltimeurl = "http://coresoccer.com/wp-content/uploads/2012/10/whistle.png"; # 32x32
  $halftimeurl = "http://www.grigsoft.com/wincmp3/help/source/images/tb_side.gif"; # 
  # $goaleesurl = "http://i633.photobucket.com/albums/uu53/metallie_blog/Soccer-Ball-16x16.png";
  $goaleesurl = "http://icons.iconarchive.com/icons/kevin-andersson/sportset/32/Soccer-icon.png";

  $green = "green";
  $red = "red";

  $open = "[b][size=11]";
  $close = "[/size][/b]";

  print BBCODE "<tr>";
  print BBCODE "<td bgcolor=\"lightblue\" align=\"center\" colspan=\"6\">$open Runde $round: $game$close</td>";
  print BBCODE "</tr>";
  # position, nick, scores, halftimes, goals, total
  print BBCODE "<tr>";
  print BBCODE "<td bgcolor=\"lightblue\" align=\"center\">$open [color=".$green."]&#9650;[/color][color=".$red."]&#9660;[/color]$close</td>"; # position
  print BBCODE "<td bgcolor=\"lightblue\">$open Navn $close</td>"; # nick
  print BBCODE "<td bgcolor=\"lightblue\" align=\"center\">[img]".$fulltimeurl."[/img]</td>"; # full-time
  print BBCODE "<td bgcolor=\"lightblue\" align=\"center\">[img]".$halftimeurl."[/img]</td>"; # half-time
  print BBCODE "<td bgcolor=\"lightblue\" align=\"center\">[img]".$goaleesurl."[/img]</td>"; # goalees
  print BBCODE "<td bgcolor=\"lightblue\" align=\"center\">$open TOT $close</td>"; # total
  print BBCODE "</tr>";

  $line = 0;
  $rank = 0;
  $lasttotal = 0;
  foreach $user (sort { $winner{$b} <=> $winner{$a} } keys %winner) {
    ($s,$rh,$ph,$gh,$ra,$pa,$ga) = split(':', $winner{$user});
    $fulltime = $rh + $ra;
    $halftime = $ph + $pa;
    $goalees = $gh + $ga;

    ++$line;
    $linecolor = "white";
    $linecolor = "beige" if ($line % 2 == 0);

    $rank = $line if ($s != $lasttotal);
    $lasttotal = $s;

    $rankcolor = "white";

    if (exists $ranking{$user}) {
      if ($ranking{$user} < $rank) {
        $rankcolor = "red";
        # moving down
      }
      elsif ($ranking{$user} > $rank) {
        $rankcolor = "green";
        # moving up
      }
      else {
        $rankcolor = "yellow";
        # steady
      }
    }
    else {
      # new ranking
      $rankcolor = "lightblue";
    }
    $ranking{$user} = $rank;

    print BBCODE "<tr>";
    print BBCODE "<td align=\"center\" bgcolor=\"".$rankcolor."\">$open$rank$close</td>"; # position
    print BBCODE "<td bgcolor=\"".$linecolor."\">$open$user$close</td>"; # nick
    print BBCODE "<td bgcolor=\"".$linecolor."\" align=\"center\">$open$fulltime$close</td>"; # full-time
    print BBCODE "<td bgcolor=\"".$linecolor."\" align=\"center\">$open$halftime$close</td>"; # half-time
    print BBCODE "<td bgcolor=\"".$linecolor."\" align=\"center\">$open$goalees$close</td>"; # goalees
    print BBCODE "<td bgcolor=\"".$linecolor."\" align=\"center\">$open$s$close</td>"; # total
    print BBCODE "</tr>";
    # print BBCODE "\n";
  }

  print BBCODE "</table></center>";
  print BBCODE "\n";

  close(BBCODE);
}



open(DATA, "resultattips.csv") || die "could not open resultattips.csv\n";
while ($line = <DATA>) {
  ++$linenum;
  next if ($line =~ /^;/);
  chomp($line);

  if ($line =~ /^#/) {
    $game = $line;
    $game =~ s/^#[ \t]*//g;
    $home = 1;
    $home = 0 if ($game !~ /^RBK/);

    # reset game-stats
    %guess = ();
    %pause = ();
    %goals = ();

    %score = ();
    %scores = ();
    $scorescount = 0;

    $forlengs = 0;
    $baklengs = 0;
    $counter = 0;

    next;
  }

  ($user,$result,$halftime,@goalees) = split(/,/, $line);

  if ($user eq "*FASIT*") {
    ++$round;
    foreach $key (keys(%guess)) {
      if ($guess{$key} eq $result) {
        if (!exists $score{$key}) { $score{$key} = 0; }
        $score{$key} += 3;
        $p = 0;
        $g = 0;
        if ($pause{$key} eq $halftime) {
          $score{$key} += 1;
          $p = 1;
        }
        @guesses = split(' ', $goals{$key});
        foreach $goalee (@goalees) {
          for ($i = 0; $i < scalar(@guesses); ++$i) {
            $guess = $guesses[$i];
            if ($guess eq $goalee) {
              $score{$key} += 1;
              $g += 1;
              $guesses[$i] = '*'.$guesses[$i];
            }
          }
        }
        if (!exists $winner{$key}) {
          $winner{$key} = "0:0:0:0:0:0:0";
        }
        ($s,$rh,$ph,$gh,$ra,$pa,$ga) = split(':', $winner{$key});
        $s += $score{$key};
        if ($home) {
          $rh += 1;
          $ph += $p;
          $gh += $g;
        } else {
          $ra += 1;
          $pa += $p;
          $ga += $g;
        }
        $winner{$key} = "$s:$rh:$ph:$gh:$ra:$pa:$ga";
      }
    }

    # guess summaries
    print "\n";
    print "Kamp: $game ".($home?"(hjemme)":"(borte)")."\n";
    print "Tips: $counter\n";
    if ($counter > 0) {
      $for = $forlengs / $counter;
      $bak = $baklengs / $counter;
      printf "Snitt: %1.0f-%1.0f ( %3.1f-%3.1f ) ($forlengs-$baklengs totalt)\n",
             $for, $bak, $for, $bak;
      print "Målscorere:\n";
  
      if ($home) {
        $scores{'-'} *= $for;
      } else {
        $scores{'-'} *= $bak;
      }
  
      $goalcount = 0;
      foreach $player (keys(%scores)) {
        $goalcount += $scores{$player};
      }
  
      if ($goalcount > 0) {
        foreach $player (sort { $scores{$b} <=> $scores{$a} } keys %scores) {
          printf "  %4.1f%% : $player{$player}\n",
                 ($scores{$player} / $goalcount) * 100.0;
        }
      }
    }

    &WriteTable();

  }
  else {
    # register game stats
    if (exists $guess{$user}) {
      push(@warnings, "Multiple entries for user $user, line $linenum.");
    }
    $guess{$user} = $result;
    $pause{$user} = $halftime;
    $goals{$user} = join(' ', @goalees);
    ($f, $b) = split('-', $result);

    $forlengs += ($f + 0);
    $baklengs += ($b + 0);
    $counter += 1;

    # fake-integrate the no-goals stats as well
    if ($home == 0 and $b == 0) {
      $scores{'-'} = 0 if (! exists $scores{'-'});
      ++$scores{'-'};
    }
    if ($home == 1 and $f == 0) {
      $scores{'-'} = 0 if (! exists $scores{'-'});
      ++$scores{'-'};
    }

    # print "SCORE: $result\n";
    foreach $goalee (@goalees) {
      # print "GOAL: $goalee\n";
      if (! exists $scores{$goalee}) {
        $scores{$goalee} = 0;
      }
      ++$scores{$goalee};
      ++$scorescount;
    }
  }



}
close(DATA);

print "\n";
print "Tabell:\n";

foreach $user (sort { $winner{$b} <=> $winner{$a} } keys %winner) {
  ($s,$rh,$ph,$gh,$ra,$pa,$ga) = split(':', $winner{$user});
  print "  $user: $s\n";
}

print "\n";

if (@warnings > 0) {
  print "\n";
  foreach $warning (@warnings) {
    print "WARNING: $warning\n";
  }
}



# <tr align="center" height="30" bgcolor="#254117"><td>[color=lawngreen][b][size=13]&#9650;[/size][/b][/color][color=red][b][size=13]&#9660;[/size][/b][/color]</td><td>[b][color=white][size=12]R01[/size][/b][/color]</td><td>[b][color=white][size=12]R00[/size][/b][/color]</td><td>[b][color=white][size=12]R00[/size][/b][/color]</td><td>[b][color=white][size=12]R00[/size][/b][/color]</td><td>[b][color=white][size=12]SUM[/size][/b][/color]</td><td>[b][color=white][size=12]%[/size][/b][/color]</td><td>[b][color=white][size=12]RPL[/size][/b][/color]</td><td>[b][color=white][size=12]NAVN/NICK[/size][/b][/color]</td></tr>
# 
# <tr align="center" height="20"><td bgcolor="indianred">[size=10][b]	51	[/size][/b]</td><td bgcolor="skyblue">[b][size=10]	65	[/size][/b]</td><td bgcolor="lightblue">[b][size=10]	14	[/size][/b]</td><td bgcolor="lightblue">[b][size=10]	0	[/size][/b]</td><td bgcolor="lightblue">[b][size=10]	0	[/size][/b]</td><td bgcolor="#FFF8C6">[b][size=10]	80	[/size][/b]</td><td bgcolor="#ECE5B6">[b][size=10]	41,18	[/size][/b]</td><td bgcolor="#C9C299">[b][size=10
