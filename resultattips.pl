#!/usr/bin/env perl

# Parse the resultattips.csv file and dump phpBB postable tables into
# round-wise html files.

$bbcode = 1; # set to 0 to produce pure html for local browsing usage

%player = ();

$player{'-'} = '-';
$player{'Alas'} = 'Jaime Alas';
$player{'Bille'} = 'Nicki Bille Nielsen';
$player{'Braathen'} = 'Erik Mellevold Bråthen';
$player{'Chibbe'} = 'John Chibuike';
$player{'Dockal'} = 'Bořek Dočkal';
$player{'Dorsin'} = 'Micke Dorsin';
$player{'Fredrik'} = 'Fredrik Midtsjø';
$player{'Gamboa'} = 'Cristian Gamboa';
$player{'Lunna'} = 'Alexander Lund Hansen';
$player{'Mike'} = 'Mike Jensen';
$player{'Mikkelsen'} = 'Tobias Mikkelsen';
$player{'Mix'} = 'Mix';
$player{'Perry'} = 'Per Joar Hansen';
$player{'Reg'} = 'Tore Reginiussen';
$player{'Roenning'} = 'Per Verner Rønning';
$player{'Selnaes'} = 'Ole Kristian Selnæs';
$player{'Svensson'} = 'Jonas Svensson';
$player{'Tarik'} = 'Tarik Elyounoussi';
$player{'Oerlund'} = 'Daniel Örlund';

@warnings = ();

%winner = ();
%roundwinner = ();

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
%ranking = ();

$linenum = 0;
$round = 0;

sub BBColor {
  ($color, $text) = (@_);
  if ($bbcode) {
    $text = "[color=".$color."]".$text."[/color]";
  }
  else {
    $text = "<font color=\"".$color."\"/>".$text."</font>";
  }
  return $text;
}

sub BBImg {
  ($url) = (@_);
  $img = "";
  if ($bbcode) {
    $img = "[img]".$url."[/img]";
  }
  else {
    $img = "<img src=\"$url\"/>";
  }
  return $img;
}

sub BBText {
  ($text) = (@_);
  if ($bbcode) {
    $text = "[b][size=11]".$text."[/size][/b]";
  }
  return $text;
}



sub WriteTable {
  ($filename, $do_rank, $heading, %table) = @_;

  print "\n";
  print "Writing BBCode to '$filename'\n";

  open(BBCODE, ">$filename") || die "could not open '$filename' for writing.";

  print BBCODE "<center>";
  print BBCODE "<table border=\"2\" bordercolor=\"black\">";

  $fulltimeurl = "http://coresoccer.com/wp-content/uploads/2012/10/whistle.png"; # 32x32
  $halftimeurl = "http://www.grigsoft.com/wincmp3/help/source/images/tb_side.gif";
  $goaleesurl = "http://icons.iconarchive.com/icons/kevin-andersson/sportset/32/Soccer-icon.png";

  $green = "green";
  $red = "red";

  print BBCODE "<tr>";
  print BBCODE "<td bgcolor=\"lightblue\" align=\"center\" colspan=\"6\">".&BBText($heading)."</td>";
  print BBCODE "</tr>";

  # position, nick, scores, halftimes, goals, total
  print BBCODE "<tr>";
  print BBCODE "<td bgcolor=\"lightblue\" align=\"center\">".&BBText(&BBColor($green, "&#9650;").&BBColor($red, "&#9660;"))."</td>";
  print BBCODE "<td bgcolor=\"lightblue\">".&BBText("Navn")."</td>";
  print BBCODE "<td bgcolor=\"lightblue\" align=\"center\">".&BBImg($fulltimeurl)."</td>";
  print BBCODE "<td bgcolor=\"lightblue\" align=\"center\">".&BBImg($halftimeurl)."</td>";
  print BBCODE "<td bgcolor=\"lightblue\" align=\"center\">".&BBImg($goaleesurl)."</td>";
  print BBCODE "<td bgcolor=\"lightblue\" align=\"center\">".&BBText("TOT")."</td>";
  print BBCODE "</tr>";

  $line = 0;
  $rank = 0;
  $lasttotal = 0;
  foreach $user (sort { $table{$b} <=> $table{$a} } keys %table) {
    ($s,$rh,$ph,$gh,$ra,$pa,$ga) = split(':', $table{$user});
    $fulltime = $rh + $ra;
    $halftime = $ph + $pa;
    $goalees = $gh + $ga;

    ++$line;
    $linecolor = "white";
    $linecolor = "beige" if ($line % 2 == 0);

    $rank = $line if ($s != $lasttotal);
    $lasttotal = $s;

    $rankcolor = $linecolor;
    if ($do_rank) {
      if (exists $ranking{$user}) {
        if ($ranking{$user} < $rank) { # moving down
          $rankcolor = "red";
        }
        elsif ($ranking{$user} > $rank) { # moving up
          $rankcolor = "green";
        }
        else { # steady
          $rankcolor = "yellow";
        }
      }
      else { # new ranking
        $rankcolor = "lightblue";
      }
      $ranking{$user} = $rank;
    }

    print BBCODE "<tr>";
    print BBCODE "<td align=\"center\" bgcolor=\"".$rankcolor."\">".&BBText("$rank")."</td>";
    print BBCODE "<td bgcolor=\"".$linecolor."\">".&BBText("$user")."</td>";
    print BBCODE "<td bgcolor=\"".$linecolor."\" align=\"center\">".&BBText("$fulltime")."</td>";
    print BBCODE "<td bgcolor=\"".$linecolor."\" align=\"center\">".&BBText("$halftime")."</td>";
    print BBCODE "<td bgcolor=\"".$linecolor."\" align=\"center\">".&BBText("$goalees")."</td>";
    print BBCODE "<td bgcolor=\"".$linecolor."\" align=\"center\">".&BBText("$s")."</td>";
    print BBCODE "</tr>";
  }

  print BBCODE "</table></center>";
  print BBCODE "\n";

  close(BBCODE);
}


open(DATA, "resultattips.csv") || die "could not open resultattips.csv\n";
while ($line = <DATA>) {
  ++$linenum;
  next if ($line =~ /^;/);
  next if ($line =~ /^$/);
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
    %roundwinner = ();

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
        if (not exists $score{$key}) { $score{$key} = 0; }
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
        ($s,$rh,$ph,$gh,$ra,$pa,$ga) = (0, 0, 0, 0, 0, 0, 0);
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
        $roundwinner{$key} = "$s:$rh:$ph:$gh:$ra:$pa:$ga";
      }
    }

    # guess summaries
    print "\n";
    print "Kamp: $game\n";
    print "Tips: $counter\n";
    if ($counter > 0) {
      $for = $forlengs / $counter;
      $bak = $baklengs / $counter;
      printf "Snitt: %1.0f-%1.0f ( %3.1f-%3.1f ) ($forlengs-$baklengs totalt)\n",
             $for, $bak, $for, $bak;
      print "Målscorere:\n";

      if ($home) {
        $scores{'-'} *= $for if (exists $scores{'-'});
      } else {
        $scores{'-'} *= $bak if (exists $scores{'-'});
      }

      $goalcount = 0;
      foreach $player (keys(%scores)) {
        $goalcount += $scores{$player};
      }

      if ($goalcount > 0) {
        foreach $player (sort { $scores{$b} <=> $scores{$a} } keys %scores) {
          if (not exists $player{$player}) {
            printf "No player '%s'\n", $player;
          }
          printf "  %4.1f%% : $player{$player}\n",
                 ($scores{$player} / $goalcount) * 100.0;
        }
      }
    }

    &WriteTable("runde-$round.html", 0, "Runde $round\n$game", %roundwinner);
    foreach $player (keys(%roundwinner)) {
      if (not exists $winner{$player}) {
        $winner{$player} = $roundwinner{$player};
      } else {
        (@w) = split(/:/, $winner{$player});
        (@r) = split(/:/, $roundwinner{$player});
        for ($i = 0; $i < 7; ++$i) {
          $w[$i] += $r[$i];
        }
        $winner{$player} = join(':', @w);
      }
    }
    &WriteTable("tabell-$round.html", 1, "Resultat etter runde $round", %winner);

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
      $scores{'-'} = 0 if (not exists $scores{'-'});
      ++$scores{'-'};
    }
    if ($home == 1 and $f == 0) {
      $scores{'-'} = 0 if (not exists $scores{'-'});
      ++$scores{'-'};
    }

    # print "SCORE: $result\n";
    foreach $goalee (@goalees) {
      # print "GOAL: $goalee\n";
      if (not exists $scores{$goalee}) {
        $scores{$goalee} = 0;
      }
      ++$scores{$goalee};
    }
  }
}
close(DATA);

print "\n";
print "Tabell:\n";

print "+----------------------+---+\n";
foreach $user (sort { $winner{$b} <=> $winner{$a} } keys %winner) {
  ($s,$rh,$ph,$gh,$ra,$pa,$ga) = split(':', $winner{$user});
  printf "| %20s | %d |\n", $user, $s;
}
print "+----------------------+---+\n";

print "\n";

if (@warnings > 0) {
  print "\n";
  foreach $warning (@warnings) {
    print "WARNING: $warning\n";
  }
}
