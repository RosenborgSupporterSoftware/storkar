#!/usr/bin/env perl

# Parse the resultattips.csv file and dump phpBB postable tables into
# round-wise html files.

$bbcode = 1; # set to 0 to produce pure html for local browsing usage

%player = ();

$player{'-'} = '-';
$player{'Alas'} = 'Jaime Alas';
$player{'Bille'} = 'Nicki Bille Nielsen';
$player{'Braathen'} = 'Erik Mellevold Br&aring;then';
$player{'Chibbe'} = 'John Chibuike';
$player{'Dockal'} = 'Bo&rcaron;ek Do&ccaron;kal';
$player{'Dorsin'} = 'Micke Dorsin';
$player{'Fredrik'} = 'Fredrik Midtsj&oslash;';
$player{'Gamboa'} = 'Cristian Gamboa';
$player{'Lunna'} = 'Alexander Lund Hansen';
$player{'Mike'} = 'Mike Jensen';
$player{'Mikkelsen'} = 'Tobias Mikkelsen';
$player{'Mix'} = 'Mix';
$player{'Perry'} = 'Per Joar Hansen';
$player{'Reg'} = 'Tore Reginiussen';
$player{'Roenning'} = 'Per Verner R&oslash;nning';
$player{'Selnaes'} = 'Ole Kristian Seln&aelig;s';
$player{'Svensson'} = 'Jonas Svensson';
$player{'Tarik'} = 'Tarik Elyounoussi';
$player{'Oerlund'} = 'Daniel &Ouml;rlund';

$logourl{'RBK'} = "http://www.altomfotball.no/jsport/multimedia/laglogo/150x88/313.png";
$logourl{'Brann'} = "http://www.altomfotball.no/jsport/multimedia/laglogo/150x88/302.png";
$logourl{'Sogndal'} = "http://www.altomfotball.no/jsport/multimedia/laglogo/150x88/326.png";


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
$forlengs_h = 0;
$baklengs_h = 0;
$counter = 0;
$counter_h = 0;

%score = ();
%scores = ();
%ranking = ();

%halftimes = ();
%fulltimes = ();

$linenum = 0;
$round = 0;


sub DeGlyph {
  ($text) = (@_);
  return $text if ($bbcode == 0);
  $text =~ s/&aelig;/æ/g;
  $text =~ s/&oslash;/ø/g;
  $text =~ s/&aring;/å/g;
  $text =~ s/&Aelig;/Æ/g;
  $text =~ s/&Oslash;/Ø/g;
  $text =~ s/&Aring;/Å/g;
  $text =~ s/&Ouml;/Ö/g;
  $text =~ s/&rcaron;/r/g; # FIXME: find caret-versions of letters
  $text =~ s/&ccaron;/c/g;
  return $text;
}


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


sub BBTextBig {
  ($text) = (@_);
  $text = &DeGlyph($text);
  if ($bbcode) {
    $text = "[b][size=20]".$text."[/size][/b]";
  }
  return $text;
}


sub BBText {
  ($text) = (@_);
  $text = &DeGlyph($text);
  if ($bbcode) {
    $text = "[b][size=11]".$text."[/size][/b]";
  }
  return $text;
}


sub WriteTable {
  ($filename, $do_rank, $heading, %table) = @_;

  # print "Writing BBCode to '$filename'\n";

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


sub WriteStats {
  ($filename) = @_;
  # print "Writing BBCode to '$filename'\n";

  $goaleesurl = "http://icons.iconarchive.com/icons/kevin-andersson/sportset/32/Soccer-icon.png";
  $muted = "lightgrey";


  open(BBCODE, ">$filename") || die "could not open '$filename' for writing.";

  print BBCODE "<center>\n";
  print BBCODE "<table border=\"0\">";
  print BBCODE "<tr>";
  print BBCODE "<td align=\"center\" valign=\"middle\">";
  $sluttres = sprintf("%1.0f-%1.0f", $for, $bak);
  $pauseres = sprintf("%1.0f-%1.0f", $for_h, $bak_h);
  print BBCODE &BBTextBig($sluttres) . "<br>" . &BBText("($pauseres)");
  print BBCODE "</td>";
  print BBCODE "<td>";
  print BBCODE "</td>";
  print BBCODE "<td colspan=\"6\" align=\"center\">";
  if (exists $logourl{$awayteam}) {
    print BBCODE &BBImg($logourl{$awayteam});
  } else {
    print BBCODE &BBText($awayteam);
  }
  print BBCODE "</td>";
  print BBCODE "</tr>";

  print BBCODE "<tr>";
  print BBCODE "<td>";
  print BBCODE "</td>";
  print BBCODE "<td>";
  print BBCODE &BBImg($goaleesurl);
  print BBCODE "</td>";
  for ($ag = 0; $ag < 6; ++$ag) {
    print BBCODE "<td align=\"center\">";
    print BBCODE &BBText("$ag");
    print BBCODE "</td>";
  }
  print BBCODE "</tr>";

  for ($hg = 0; $hg < 6; ++$hg) {
    print BBCODE "<tr>";
    if ($hg == 0) {
      print BBCODE "<td rowspan=\"6\">";
      if (exists $logourl{$hometeam}) {
        print BBCODE &BBImg($logourl{$hometeam});
      } else {
        print BBCODE &BBText(join("<br>", split("", $hometeam)));
      }
      print BBCODE "</td>";
    }
    print BBCODE "<td align=\"center\">";
    print BBCODE &BBText("$hg");
    print BBCODE "</td>";
    for ($ag = 0; $ag < 6; ++$ag) {
      $scorestr = sprintf("%d-%d", $hg, $ag);
      $cellcolor = "yellow";
      if ($home) {
        if ($hg > $ag) {
          $cellcolor = "green";
        } elsif ($hg < $ag) {
          $cellcolor = "red";
        }
      }
      else {
        if ($hg > $ag) {
          $cellcolor = "red";
        } elsif ($hg < $ag) {
          $cellcolor = "green";
        }
      }
      $guesses = 0;
      $guesses = $fulltimes{$scorestr} if exists $fulltimes{$scorestr};
      print BBCODE "<td align=\"center\" bgcolor=\"$cellcolor\">";
      if (exists $fulltimes{$scorestr}) {
        printf BBCODE &BBText("$guesses");
      } else {
        printf BBCODE &BBColor($cellcolor,&BBText($scorestr));
      }
      print BBCODE "</td>";
    }
    print BBCODE "</tr>";
  }
  print BBCODE "</table>\n";
  print BBCODE "</center>\n";

  return if ($counter == 0);

  if ($goalcount > 0) {
    print BBCODE "\n\n";
    print BBCODE "<center>\n";
    # goalee stats
    print BBCODE "<table border=\"0\" bordercolor=\"black\">";
    print BBCODE "<tr bgcolor=\"lightblue\">";
    print BBCODE "<td align=\"center\">";
    print BBCODE &BBText("#");
    print BBCODE "</td>";
    print BBCODE "<td align=\"center\">";
    print BBCODE &BBText("%");
    print BBCODE "</td>";
    print BBCODE "<td>";
    print BBCODE &BBText("Spiller");
    print BBCODE "</td>";
    print BBCODE "</tr>";

    $row = 0;
    foreach $player (sort { $scores{$b} <=> $scores{$a} } keys %scores) {
      ++$row;
      $rowcolor = "white";
      if ($row % 2 == 1) {
        $rowcolor = "beige";
      }

      print BBCODE "<tr bgcolor=\"$rowcolor\">";
      print BBCODE "<td align=\"center\">" . &BBText(sprintf("%.3g", $scores{$player})) . "</td>";
      print BBCODE "<td align=\"center\">" . &BBText(sprintf("%4.1f%%", ($scores{$player} / $goalcount) * 100.0)) .  "</td>";
      print BBCODE "<td>" . &BBText($player{$player}) . "</td>";
      print BBCODE "</tr>";
    }
    print BBCODE "</table>\n";
    print BBCODE "</center>\n";
  }

  print BBCODE "\n";

  printf BBCODE "Snitt slutt: %1.0f-%1.0f (%3.1f-%3.1f) (%d-%d p&aring; %d tips)\n",
                $for, $bak, $for, $bak,
                $forlengs, $baklengs, $counter;
  if ($counter_h > 0) {
    printf BBCODE "Snitt pause: %1.0f-%1.0f (%3.1f-%3.1f) (%d-%d p&aring; %d tips)\n",
                  $for_h, $bak_h, $for_h, $bak_h,
                  $forlengs_h, $baklengs_h, $counter_h;
  }
  print BBCODE "\n";
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

    if ($game =~ m/^(.*) - (.*) 2013/) {
      $hometeam = $1;
      $awayteam = $2;
    }
    $home = 0;
    $home = 1 if ($hometeam =~ m/^RBK$/);

    # reset game-stats
    %guess = ();
    %pause = ();
    %goals = ();

    %score = ();
    %scores = ();
    %roundwinner = ();

    %halftimes = ();
    %fulltimes = ();

    $forlengs = 0;
    $baklengs = 0;
    $forlengs_h = 0;
    $baklengs_h = 0;
    $counter = 0;
    $counter_h = 0;

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
    if ($counter > 0) {
      $for = $forlengs / $counter;
      $bak = $baklengs / $counter;
      printf "Snitt slutt: %1.0f-%1.0f (%3.1f-%3.1f) (%d-%d på %d tips)\n",
             $for, $bak, $for, $bak,
             $forlengs, $baklengs, $counter;
      if ($counter_h > 0) {
        $for_h = $forlengs_h / $counter_h;
        $bak_h = $baklengs_h / $counter_h;
        printf "Snitt pause: %1.0f-%1.0f (%3.1f-%3.1f) (%d-%d på %d tips)\n",
               $for_h, $bak_h, $for_h, $bak_h,
               $forlengs_h, $baklengs_h, $counter_h;
      }
      print "Målscorere:\n";

      if ($home) {
        $scores{'-'} *= $for if (exists $scores{'-'});
      } else {
        $scores{'-'} *= $bak if (exists $scores{'-'});
      }

      $goalcount = 0;
      foreach $player (keys(%scores)) {
        if ($player !~ /^-$/) {
          $goalcount += $scores{$player}
        }
      }

      if ($goalcount > 0) {
        foreach $player (sort { $scores{$b} <=> $scores{$a} } keys %scores) {
          if (not exists $player{$player}) {
            printf "No player '%s'\n", $player;
          }
          printf "  %4.1f%% : $player{$player} (%.3g)\n",
                 ($scores{$player} / $goalcount) * 100.0, $scores{$player};
        }
      }

      print "\n";
      print "       $awayteam\n";
      print "  ___0___1___2___3___4___5\n";
      for ($hg = 0; $hg < 6; ++$hg) {
        print "$hg: ";
        for ($ag = 0; $ag < 6; ++$ag) {
          $scorestr = sprintf("%d-%d", $hg, $ag);
          $guesses = 0;
          $guesses = $fulltimes{$scorestr} if exists $fulltimes{$scorestr};
          if (exists $fulltimes{$scorestr}) {
            printf "%3d ", $guesses;
          } else {
            printf "%4s", $scorestr;
          }
        }
        print "\n";
      }
      print "\n";

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

    &WriteStats("stats-$round.html");

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

    $fulltimes{$result} = 0 if (not exists $fulltimes{$result});
    $fulltimes{$result} += 1;

    $forlengs += ($f + 0);
    $baklengs += ($b + 0);
    if ($halftime !~ /^-$/) {
      $halftimes{$halftime} = 0 if (not exists $halftimes{$halftime});
      $halftimes{$halftime} += 1;
      ($fh, $bh) = split('-', $halftime);
      $forlengs_h += ($fh + 0);
      $baklengs_h += ($bh + 0);
      $counter_h += 1;
    }
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
