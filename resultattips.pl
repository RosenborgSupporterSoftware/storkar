#!/usr/bin/env perl

# Parse the resultattips.csv file and dump phpBB postable tables into
# round-wise html files.
#
# Mye norsk i dette scriptet da det i fremtiden sikkert må skje en handover
# til en annen rbkweb-bruker.
#
# TODO:
# - Norske bokstaver for både HTML og BBCode
# - Sortere rundetabell og resultattabell på pauseresultat foran målscorere
# - Målscoreres popularitet i endring over tid
#   &#9601;&#9602;&#9603;&#9604;&#9605;&#9606;&#9607;&#9608;
# - Automatisk utregning av rbkweb.no's snitt-tips (målscorere)
#   - Opsjon for å vekte tipspoolen etter brukerenes poeng
#   - Opsjon for å filtrere tipsene etter brukerenes poeng
# - Mulighet for å liste opp alle som har deltatt men som ikke har fått
#   poeng ennå.
# - Gjøre --bbcode til en kommandolinjeopsjon
# - La resultattips-filen være input-argument
# - Refaktoriser scriptet grundig!

$bbcode = 1; # set to 0 to produce pure html for local browsing usage
$matrixsize = 7;

%player = ();

$player{'-'} = '-';
$player{'Alas'} = 'Jaime Alas'; # Jaime Enrique Alas Morales
$player{'Bille'} = 'Nicki Bille Nielsen'; # Nicki Niels Bille Nielsen
$player{'Berntsen'} = 'Daniel Berntsen';
$player{'Braathen'} = 'Erik Mellevold Br&aring;then';
$player{'Chibbe'} = 'John Chibuike';
$player{'Dockal'} = 'Bo&rcaron;ek Do&ccaron;kal';
$player{'Dorsin'} = 'Micke Dorsin'; # Mikael Frank Dorsin
$player{'Fredrik'} = 'Fredrik Midtsj&oslash;';
$player{'Gamboa'} = 'Cristian Gamboa';
$player{'Lunna'} = 'Alexander Lund Hansen';
$player{'Mike'} = 'Mike Jensen';
$player{'Mikkelsen'} = 'Tobias Mikkelsen';
$player{'Mix'} = 'Mix'; # Mikkel Diskerud
$player{'Moe'} = 'Brede Moe'; # Brede Mathias Moe
$player{'Perry'} = 'Per Joar Hansen';
$player{'Reg'} = 'Tore Reginiussen';
$player{'Roenning'} = 'Per Verner R&oslash;nning';
$player{'Selnaes'} = 'Ole Kristian Seln&aelig;s';
$player{'Svensson'} = 'Jonas Svensson';
$player{'Tarik'} = 'Tarik Elyounoussi';
$player{'Oerlund'} = 'Daniel &Ouml;rlund';

$logourl{'Aalesund'} = "http://www.altomfotball.no/jsport/multimedia/laglogo/150x88/403.png";
$logourl{'Brann'} = "http://www.altomfotball.no/jsport/multimedia/laglogo/150x88/302.png";
$logourl{'Haugesund'} = "http://www.altomfotball.no/jsport/multimedia/laglogo/150x88/306.png";
$logourl{'Hoenefoss'} = "http://www.altomfotball.no/jsport/multimedia/laglogo/150x88/327.png";
$logourl{'Lillestroem'} = "http://www.altomfotball.no/jsport/multimedia/laglogo/150x88/308.png";
$logourl{'Molde'} = "http://www.altomfotball.no/jsport/multimedia/laglogo/150x88/309.png";
$logourl{'Odd'} = "http://www.altomfotball.no/jsport/multimedia/laglogo/150x88/311.png";
$logourl{'RBK'} = "http://www.altomfotball.no/jsport/multimedia/laglogo/150x88/313.png";
$logourl{'Sandnes Ulf'} = "http://www.altomfotball.no/jsport/multimedia/laglogo/150x88/496.png";
$logourl{'Sarpsborg 08'} = "http://www.altomfotball.no/jsport/multimedia/laglogo/150x88/541.png";
$logourl{'Sogndal'} = "http://www.altomfotball.no/jsport/multimedia/laglogo/150x88/326.png";
$logourl{'Start'} = "http://www.altomfotball.no/jsport/multimedia/laglogo/150x88/305.png";
$logourl{'Stroemsgodset'} = "http://www.altomfotball.no/jsport/multimedia/laglogo/150x88/328.png";
$logourl{'Tromsoe'} = "http://www.altomfotball.no/jsport/multimedia/laglogo/150x88/315.png";
$logourl{'Viking'} = "http://www.altomfotball.no/jsport/multimedia/laglogo/150x88/303.png";
$logourl{'Vaalerenga'} = "http://www.altomfotball.no/jsport/multimedia/laglogo/150x88/314.png";

@warnings = ();

%winner = ();
%roundwinner = ();

$game = "";
$home = 1;

$wins = 0;
$draws = 0;
$losses = 0;
$wins_h = 0;
$draws_h = 0;
$losses_h = 0;

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
#  $text =~ s/&ae;/æ/g;
#  $text =~ s/&oe;/ø/g;
#  $text =~ s/&aa;/å/g;
#  $text =~ s/&AE;/Æ/g;
#  $text =~ s/&OE;/Ø/g;
#  $text =~ s/&AA;/Å/g;

  $text =~ s/&ae;/�/g;
  $text =~ s/&oe;/�/g;
  $text =~ s/&o\.\.;/�/g;
  $text =~ s/&aa;/�/g;
  $text =~ s/&AE;/�/g;
  $text =~ s/&OE;/�/g;
  $text =~ s/&AA;/�/g;
  $text =~ s/&O\.\.;/�/g;

  $text =~ s/&c;/,/g;
  $text =~ s/&rcaron;/&#345;/g;
  $text =~ s/&ccaron;/&#269;/g;

  return $text if ($bbcode == 0);
  $text =~ s/&aelig;/æ/g;
  $text =~ s/&oslash;/ø/g;
  $text =~ s/&aring;/å/g;
  $text =~ s/&Aelig;/Æ/g;
  $text =~ s/&Oslash;/Ø/g;
  $text =~ s/&Aring;/Å/g;
  $text =~ s/&Ouml;/Ö/g;
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
  } else {
    $text = "<b><font size=+3>".$text."</font></b>";
  }
  return $text;
}


sub BBText {
  ($text) = (@_);
  $text = &DeGlyph($text);
  if ($bbcode) {
    $text = "[b][size=11]".$text."[/size][/b]";
  } else {
    $text = "<b><font size=-1>".$text."</font></b>";
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
  print BBCODE "<td bgcolor=\"lightblue\" align=\"center\" colspan=\"$matrixsize\">".&BBText($heading)."</td>";
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
  foreach $user (sort { $table{$b} <=> $table{$a} or $table{$b} cmp $table{$a} } keys %table) {
    ($s,$fulltime,$halftime,$goalees,$rh,$ph,$gh,$ra,$pa,$ga) = split(':', $table{$user});

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
    print BBCODE "<td bgcolor=\"".$linecolor."\">".&BBText(&DeGlyph($user))."</td>";
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
  print BBCODE &BBTextBig($sluttres);
  if ($bbcode) {
    print BBCODE "\n";
  } else {
    print BBCODE "<br>";
  }
  print BBCODE &BBText("($pauseres)");
  print BBCODE "</td>";
  print BBCODE "<td>";
  print BBCODE "</td>";
  print BBCODE "<td colspan=\"$matrixsize\" align=\"center\">";
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
  for ($ag = 0; $ag < $matrixsize; ++$ag) {
    print BBCODE "<td align=\"center\">";
    print BBCODE &BBText("$ag");
    print BBCODE "</td>";
  }
  print BBCODE "</tr>";

  for ($hg = 0; $hg < $matrixsize; ++$hg) {
    print BBCODE "<tr>";
    if ($hg == 0) {
      print BBCODE "<td rowspan=\"$matrixsize\">";
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
    for ($ag = 0; $ag < $matrixsize; ++$ag) {
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

  $cellcolor = "lightblue";
  print BBCODE "<center>\n";
  print BBCODE "<table border=\"0\" bgcolor=\"white\">";
  print BBCODE "<tr>";
  print BBCODE "<td bgcolor=\"$cellcolor\"></td>";
  print BBCODE "<td bgcolor=\"$cellcolor\">".&BBText("90. min")."</td>";
  print BBCODE "<td bgcolor=\"$cellcolor\">".&BBText("45. min")."</td>";
  print BBCODE "</tr>";

  $cellcolor = "beige";
  print BBCODE "<tr>";
  print BBCODE "<td bgcolor=\"$cellcolor\" align=\"right\">".&BBText("Tips")."</td>";
  print BBCODE "<td bgcolor=\"$cellcolor\" align=\"center\">".&BBText("$counter")."</td>";
  print BBCODE "<td bgcolor=\"$cellcolor\" align=\"center\">".&BBText("$counter_h")."</td>";
  print BBCODE "</tr>";

  $cellcolor = "white";
  print BBCODE "<tr>";
  print BBCODE "<td bgcolor=\"$cellcolor\" align=\"right\">".&BBText("Seire")."</td>";
  print BBCODE "<td bgcolor=\"$cellcolor\" align=\"center\">".&BBText("$wins")."</td>";
  print BBCODE "<td bgcolor=\"$cellcolor\" align=\"center\">".&BBText("$wins_h")."</td>";
  print BBCODE "</tr>";

  $cellcolor = "beige";
  print BBCODE "<tr>";
  print BBCODE "<td bgcolor=\"$cellcolor\" align=\"right\">".&BBText("Uavgjort")."</td>";
  print BBCODE "<td bgcolor=\"$cellcolor\" align=\"center\">".&BBText("$draws")."</td>";
  print BBCODE "<td bgcolor=\"$cellcolor\" align=\"center\">".&BBText("$draws_h")."</td>";
  print BBCODE "</tr>";

  $cellcolor = "white";
  print BBCODE "<tr>";
  print BBCODE "<td bgcolor=\"$cellcolor\" align=\"right\">".&BBText("Tap")."</td>";
  print BBCODE "<td bgcolor=\"$cellcolor\" align=\"center\">".&BBText("$losses")."</td>";
  print BBCODE "<td bgcolor=\"$cellcolor\" align=\"center\">".&BBText("$losses_h")."</td>";
  print BBCODE "</tr>";

  $cellcolor = "beige";
  print BBCODE "<tr>";
  print BBCODE "<td bgcolor=\"$cellcolor\" align=\"right\">".&BBText("Resultat")."</td>";
  printf BBCODE "<td bgcolor=\"$cellcolor\" align=\"center\">".&BBText("%1.0f-%1.0f")."</td>", $for, $bak;
  printf BBCODE "<td bgcolor=\"$cellcolor\" align=\"center\">".&BBText("%1.0f-%1.0f")."</td>", $for_h, $bak_h;
  print BBCODE "</tr>";

  $cellcolor = "white";
  print BBCODE "<tr>";
  print BBCODE "<td bgcolor=\"$cellcolor\" align=\"right\">".&BBText("Eksakt")."</td>";
  printf BBCODE "<td bgcolor=\"$cellcolor\" align=\"center\">".&BBText("%3.1f-%3.1f")."</td>", $for, $bak;
  printf BBCODE "<td bgcolor=\"$cellcolor\" align=\"center\">".&BBText("%3.1f-%3.1f")."</td>", $for_h, $bak_h;
  print BBCODE "</tr>";

  $cellcolor = "beige";
  print BBCODE "<tr>";
  print BBCODE "<td bgcolor=\"$cellcolor\" align=\"right\">".&BBText("Sum m&aring;l")."</td>";
  print BBCODE "<td bgcolor=\"$cellcolor\" align=\"center\">".&BBText("$forlengs-$baklengs")."</td>";
  print BBCODE "<td bgcolor=\"$cellcolor\" align=\"center\">".&BBText("$forlengs_h-$baklengs_h")."</td>";
  print BBCODE "</tr>";

  print BBCODE "</table>\n";
  print BBCODE "</center>\n";


  if ($goalcount > 0) {
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
      $scoresstr = sprintf("%6.1f", $scores{$player});
      $scoresstr =~ s/\.0$//;
      print BBCODE "<td align=\"center\">" . &BBText($scoresstr) . "</td>";
      print BBCODE "<td align=\"center\">" . &BBText(sprintf("%4.1f%%", ($scores{$player} / $goalcount) * 100.0)) .  "</td>";
      print BBCODE "<td>" . &BBText($player{$player}) . "</td>";
      print BBCODE "</tr>";
    }
    print BBCODE "</table>\n";
    print BBCODE "</center>\n";
  }

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

    $wins = 0;
    $draws = 0;
    $losses = 0;
    $wins_h = 0;
    $draws_h = 0;
    $losses_h = 0;

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
          $goaleestr = $goalee;
          for ($i = 0; $i < scalar(@guesses); ++$i) {
            $guess = $guesses[$i];
            if ($guess eq $goaleestr) {
              $score{$key} += 1;
              $g += 1;
              $guesses[$i] = '*'.$guesses[$i];
              $goaleestr = 'break';
            }
          }
        }
        ($s,$rb,$pb,$gb,$rh,$ph,$gh,$ra,$pa,$ga) = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0);
        $s += $score{$key};
        if ($home) {
          $rh += 1;
          $ph += $p;
          $gh += $g;
          $rb += 1;
          $pb += $p;
          $gb += $g;
        } else {
          $ra += 1;
          $pa += $p;
          $ga += $g;
          $rb += 1;
          $pb += $p;
          $gb += $g;
        }
        $roundwinner{$key} = "$s:$rb:$pb:$gb:$rh:$ph:$gh:$ra:$pa:$ga";
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
      print "  ";
      for ($ag = 0; $ag < $matrixsize; ++$ag) {
        print "___$ag";
      }
      print "\n";
      for ($hg = 0; $hg < $matrixsize; ++$hg) {
        print "$hg: ";
        for ($ag = 0; $ag < $matrixsize; ++$ag) {
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
        for ($i = 0; $i < 10; ++$i) {
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

    if ($home) {
      $wins += 1 if ($f > $b);
      $draws += 1 if ($f == $b);
      $losses += 1 if ($f < $b);
    } else {
      $wins += 1 if ($f < $b);
      $draws += 1 if ($f == $b);
      $losses += 1 if ($f > $b);
    }

    if ($halftime !~ /^-$/) {
      $halftimes{$halftime} = 0 if (not exists $halftimes{$halftime});
      $halftimes{$halftime} += 1;
      ($fh, $bh) = split('-', $halftime);
      $forlengs_h += ($fh + 0);
      $baklengs_h += ($bh + 0);
      $counter_h += 1;

      if ($home) {
        $wins_h += 1 if ($fh > $bh);
        $draws_h += 1 if ($fh == $bh);
        $losses_h += 1 if ($fh < $bh);
      } else {
        $wins_h += 1 if ($fh < $bh);
        $draws_h += 1 if ($fh == $bh);
        $losses_h += 1 if ($fh > $bh);
      }
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
  ($s,$rb,$pb,$gb,$rh,$ph,$gh,$ra,$pa,$ga) = split(':', $winner{$user});
  printf "| %20s | %d |\n", &DeGlyph($user), $s;
}
print "+----------------------+---+\n";

print "\n";

if (@warnings > 0) {
  print "\n";
  foreach $warning (@warnings) {
    print "WARNING: $warning\n";
  }
}
