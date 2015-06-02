#!/usr/bin/env perl

# Parse the resultattips.csv file and dump phpBB postable tables into
# round-wise html files.
#
# Mye norsk i dette scriptet da det i fremtiden sikkert må skje en handover
# til en annen rbkweb-bruker.
#
# TODO:
# - Norske bokstaver for både HTML og BBCode (bruk &# unicode values)
# - Sortere rundetabell og resultattabell på pauseresultat foran målscorere
# - Automatisk utregning av rbkweb.no's snitt-tips (målscorere)
#   - Opsjon for å vekte tipspoolen etter brukerenes poeng
#   - Opsjon for å filtrere tipsene etter brukerenes poeng
# - Mulighet for å liste opp alle som har deltatt men som ikke har fått
#   poeng ennå.
# - Gjøre --bbcode til en kommandolinjeopsjon
# - La resultattips-filen være input-argument
# - Refaktoriser scriptet grundig!
# - Skriv ut tips utenfor matrisen.
# - St�tt � skrive gangefaktor bak m�lscrorere for � duplisere de ut
# - BB-code-fungerende br->\n

$bbcode = 1; # set to 0 to produce pure html for local browsing usage
$matrixmaxsize = 12;
$trustsize = 6;

$matrixminwidth = 0;
$matrixminheight = 0;

$fontsize = 11;

%player = (
  '-'          => '-',
  'Alas'       => 'Jaime Alas',  # Jaime Enrique Alas Morales
  'Bille'      => 'Nicki Bille Nielsen',  # Nicki Niels Bille Nielsen
  'Berntsen'   => 'Daniel Berntsen',
  'Braathen'   => 'Erik Mellevold Br&aring;then',
  'Chibbe'     => 'John Chibuike',
  'Dockal'     => 'Bo&rcaron;ek Do&ccaron;kal',
  'Dorsin'     => 'Micke Dorsin',  # Mikael Frank Dorsin
  'Fredrik'    => 'Fredrik Midtsj&oslash;',
  'Gamboa'     => 'Cristian Gamboa',
  'JIH'        => 'Jon Inge H&oslash;iland',
  'Lunna'      => 'Alexander Lund Hansen',
  'Mike'       => 'Mike Jensen',
  'Mikkelsen'  => 'Tobias Mikkelsen',
  'Mix'        => 'Mix',  # Mikkel Diskerud
  'Moe'        => 'Brede Moe',  # Brede Mathias Moe
  'OKS'        => 'Ole Kristian Seln&aelig;s',
  'Perry'      => 'Per Joar Hansen',
  'PVR'        => 'Per Verner R&oslash;nning',
  'Reg'        => 'Tore Reginiussen',
  'Strandberg' => 'Stefan Strandberg',
  'Svensson'   => 'Jonas Svensson',
  'Tarik'      => 'Tarik Elyounoussi',
  'Oerlund'    => 'Daniel &Ouml;rlund'
);

$urlprefix = "http://www.altomfotball.no/jsport/multimedia/laglogo/150x88/";
%logourl = (
  'Aalesund'      => $urlprefix."403.png",
  'Brann'         => $urlprefix."302.png",
  'Haugesund'     => $urlprefix."306.png",
  'Hoenefoss'     => $urlprefix."327.png",
  'Lillestroem'   => $urlprefix."308.png",
  'Molde'         => $urlprefix."309.png",
  'Odd'           => $urlprefix."311.png",
  'RBK'           => $urlprefix."313.png",
  'Sandnes Ulf'   => $urlprefix."496.png",
  'Sarpsborg 08'  => $urlprefix."541.png",
  'Sogndal'       => $urlprefix."326.png",
  'Start'         => $urlprefix."305.png",
  'Stroemsgodset' => $urlprefix."328.png",
  'Tromsoe'       => $urlprefix."315.png",
  'Viking'        => $urlprefix."303.png",
  'Vaalerenga'    => $urlprefix."314.png",
  'Strindheim'    => "http://strindheimtoppfotball.no/wp-content/uploads/2013/03/Strindheim_Idrettslag-100x94.png"
);

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
%tillit = ();

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
  my ($color, $text) = (@_);
  if ($bbcode) {
    $text = "[color=".$color."]".$text."[/color]";
  }
  else {
    $text = "<font color=\"".$color."\"/>".$text."</font>";
  }
  return $text;
}


sub BBImg {
  my ($url) = (@_);
  my $img = "";
  if ($bbcode) {
    $img = "[img]".$url."[/img]";
  }
  else {
    $img = "<img src=\"$url\"/>";
  }
  return $img;
}


sub BBTextBig {
  my ($text) = (@_);
  $text = &DeGlyph($text);
  if ($bbcode) {
    $text = "[b][size=20]".$text."[/size][/b]";
  } else {
    $text = "<b><font size=+3>".$text."</font></b>";
  }
  return $text;
}


sub BBColorOpen {
  my ($color) = (@_);
  if ($bbcode) {
    return "[color=".$color."]";
  } else {
    return "<font color=\"$color\">";
  }
}


sub BBColorClose {
  if ($bbcode) {
    return "[/color]";
  } else {
    return "</font>";
  }
}

sub BBTillitGraf {
  my ($text) = (@_);

  my $level = 0;
  my $lastcolor = 'black';
  my $color = 'black';
  my $newtext = "";

  foreach $char (split("", substr($text,-$trustsize))) {
    if (int($char) >= $level) {
      $color = 'green';
    } else {
      $color = 'red';
    }
    $level = int($char);
    if ($color ne $lastcolor) {
      $newtext = $newtext . &BBColorClose() if ($lastcolor ne 'black');
      $newtext = $newtext . &BBColorOpen($color);
      $lastcolor = $color;
    }

    if ($char eq "0") {
      $newtext = $newtext . "&#12288;";
    } else {
      $newtext = $newtext . "&#960" . $char . ";";
    }
  }
  $newtext = $newtext . &BBColorClose();
  return $newtext;
}

sub TillitNumber {
  my ($percentage) = (@_);
  my $limit = 1.0;
  for (my $i = 1; $i < 8; ++$i) {
    return "$i" if ($percentage < $limit);
    $limit *= 2.154; # 2.51&5 = 100, 1.9305^7 = 100, 2.154^6 = 100
  }
  return "8";
}


sub BBText {
  my ($text) = (@_);
  $text = &DeGlyph($text);
  if ($bbcode) {
    $text = "[b][size=$fontsize]".$text."[/size][/b]";
  } else {
    $text = "<b><font size=-1>".$text."</font></b>";
  }
  return $text;
}


sub WriteTable {
  my ($filename, $do_rank, $heading, %table) = @_;

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
  foreach $user (sort { $table{$b} <=> $table{$a} or $table{$b} cmp $table{$a} } keys %table) {
    ($s,$fulltime,$halftime,$goalees,$rh,$ph,$gh,$ra,$pa,$ga) = split(':', $table{$user});

    ++$line;
    $linecolor = "white";
    $linecolor = "beige" if (($line % 2) == 0);

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
  my ($filename) = @_;
  # print "Writing BBCode to '$filename'\n";

  $goaleesurl = "http://icons.iconarchive.com/icons/kevin-andersson/sportset/32/Soccer-icon.png";
  $muted = "lightgrey";

  $matrixminwidth = 6;
  $matrixminheight = 6;
  $maxcount = 0;
  for ($hg = 0; $hg <= $matrixmaxsize; ++$hg) {
    for ($ag = 0; $ag <= $matrixmaxsize; ++$ag) {
      $scorestr = sprintf("%d-%d", $hg, $ag);
      if (exists $fulltimes{$scorestr}) {
        $matrixminheight = ($hg + 1) if ($hg + 1) > $matrixminheight;
        $matrixminwidth = ($ag + 1) if ($ag + 1) > $matrixminwidth;
        $maxcount = $fulltimes{$scorestr} if $fulltimes{$scorestr} > $maxcount;
      }
    }
  }

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
  print BBCODE "<td colspan=\"$matrixminwidth\" align=\"center\">";
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
  for ($ag = 0; $ag < $matrixminwidth; ++$ag) {
    print BBCODE "<td align=\"center\">";
    print BBCODE &BBText("$ag");
    print BBCODE "</td>";
  }
  print BBCODE "</tr>";

  for ($hg = 0; $hg < $matrixminheight; ++$hg) {
    print BBCODE "<tr>";
    if ($hg == 0) {
      print BBCODE "<td rowspan=\"$matrixminheight\">";
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
    for ($ag = 0; $ag < $matrixminwidth; ++$ag) {
      $scorestr = sprintf("%d-%d", $hg, $ag);
      $cellcolor = "#ffff00";
      if ($home) {
        if ($hg > $ag) {
          $cellcolor = "#00cc00";
        } elsif ($hg < $ag) {
          $cellcolor = "#ff0000";
        }
      }
      else {
        if ($hg > $ag) {
          $cellcolor = "#ff0000";
        } elsif ($hg < $ag) {
          $cellcolor = "#00cc00";
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


  if ($goalcount > 0 and $round != 5) {
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
    print BBCODE "<td align=\"center\">";
    print BBCODE &BBText("Spiller");
    print BBCODE "</td>";
    print BBCODE "<td align=\"center\">";
    print BBCODE &BBText("Tillit");
    print BBCODE "</td>";
    print BBCODE "</tr>";

    foreach $player (keys %tillit) {
      $tillit{$player} = $tillit{$player} . "0";
    }

    $row = 0;
    foreach $player (sort { $scores{$b} <=> $scores{$a} } keys %scores) {
      ++$row;
      $rowcolor = "white";
      if (($row % 2) == 1) {
        $rowcolor = "beige";
      }

      $percentage = ($scores{$player} / $goalcount) * 100.0;
      $percentage *= $for if $home;
      $percentage *= $bak if not $home;
      $number = &TillitNumber($percentage);

      $tillit{$player} = "0" if not exists $tillit{$player};
      $tillit{$player} =~ s/0$/$number/;

      # print "Spiller: $player{$player}: $tillit{$player} ($percentage ($scores{$player} / $goalcount) for $for bak $bak\n";

      # $tillit = $percentage / 100.0;
      # $tillit = 1.0 if ($tillit > 1.0); # taket er satt p� 100%
      # $tillit = sprintf("%1.0f", $tillit * 7.0); # gir tegn 0-7 (8 rendres feil)
      print BBCODE "<tr bgcolor=\"$rowcolor\">";
      $scoresstr = sprintf("%6.1f", $scores{$player});
      $scoresstr =~ s/\.0$//;
      print BBCODE "<td align=\"center\">" . &BBText($scoresstr) . "</td>";

      print BBCODE "<td align=\"center\">" . &BBText(sprintf("%4.1f%%", $percentage)) .  "</td>";
      print BBCODE "<td>" . &BBText($player{$player}) . "</td>";
      print BBCODE "<td align=\"right\">";
      print BBCODE &BBText(&BBTillitGraf($tillit{$player}));
      print BBCODE "</td>";
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

    # console guess summaries
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
        $scores{'-'} *= $for if exists $scores{'-'};
      } else {
        $scores{'-'} *= $bak if exists $scores{'-'};
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
          if ($home) {
            $percentage = ($scores{$player} / $goalcount) * 100.0 * $for;
          } else {
            $percentage = ($scores{$player} / $goalcount) * 100.0 * $bak;
          }
          printf "  %4.1f%% : $player{$player} (%.3g)   %s\n",
                 $percentage, $scores{$player}, $tillit{$player};
        }
      }

      $matrixminwidth = 6;
      $matrixminheight = 6;
      $maxcount = 0;
      for ($hg = 0; $hg <= $matrixmaxsize; ++$hg) {
        for ($ag = 0; $ag <= $matrixmaxsize; ++$ag) {
          $scorestr = sprintf("%d-%d", $hg, $ag);
          if (exists $fulltimes{$scorestr}) {
            $matrixminheight = ($hg + 1) if ($hg + 1) > $matrixminheight;
            $matrixminwidth = ($ag + 1) if ($ag + 1) > $matrixminwidth;
            $maxcount = $fulltimes{$scorestr} if $fulltimes{$scorestr} > $maxcount;
          }
        }
      }

      print "\n";
      print "       $awayteam\n";
      print "  ";
      for ($ag = 0; $ag < $matrixminwidth; ++$ag) {
        print "___$ag";
      }
      print "\n";
      for ($hg = 0; $hg < $matrixminheight; ++$hg) {
        print "$hg: ";
        for ($ag = 0; $ag < $matrixminwidth; ++$ag) {
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
      print "max-count: $maxcount\n";

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
      print "No goals from $user\n";
      $scores{'-'} = 0 if (not exists $scores{'-'});
      ++$scores{'-'};
    }
    if ($home == 1 and $f == 0) {
      print "No goals from $user\n";
      $scores{'-'} = 0 if (not exists $scores{'-'});
      ++$scores{'-'};
    }

    # print "SCORE: $result\n";
    foreach $goalee (@goalees) {
      # print "GOAL: $goalee\n";
      $scores{$goalee} = 0 if not exists $scores{$goalee};
      ++$scores{$goalee};
    }
  }
}
close(DATA);

print "\n";
if ($halftime != "-") {
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
}
