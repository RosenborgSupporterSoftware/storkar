#!/usr/bin/env perl

%player = ();

$player{'Bille'} = 'Nicki Bille Nielsen';
$player{'Billie'} = 'Nicki Bille Nielsen';
$player{'Ørlund'} = 'Daniel Örlund';
$player{'Bråthen'} = 'Erik Mellevold Bråthen';
$player{'Dockal'} = 'Bořek Dočkal';
$player{'Dorsin'} = 'Micke Dorsin';
$player{'Lunna'} = 'Alexander Lund Hansen';
$player{'Perry'} = 'Per Joar Hansen';
$player{'Reginiussen'} = 'Tore Reginiussen';
$player{'Tarik'} = 'Tarik Elyounoussi';
$player{'Mikkelsen'} = 'Tobias Mikkelsen';
$player{'Tobias'} = 'Tobias Mikkelsen';
$player{'Svensson'} = 'Jonas Svensson';
$player{'Selnæs'} = 'Ole Kristian Selnæs';
$player{'Mix'} = 'Mix';
$player{'Fredrik'} = 'Fredrik Midtsjø';
$player{'Jensen'} = 'Mike Jensen';
$player{'Rønning'} = 'Per Verner Rønning';
$player{'Gamboa'} = 'Cristian Gamboa';
$player{'-'} = '-';

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

$linenum = 0;

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
    print "Kamp: $game\n";
    print "Tips: $counter\n";
    if ($counter > 0) {
      $for = $forlengs / $counter;
      $bak = $baklengs / $counter;
      printf "Snitt: %1.0f-%1.0f ( %3.1f-%3.1f ) ($forlengs-$baklengs totalt)\n",
             $for, $bak, $for, $bak;
      print "Målscorere:\n";
  
      $scores{'-'} *= $bak;
  
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
    if ($home == 1 and $h == 0) {
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
  printf "  $user: $s\n";
}

if (@warnings > 0) {
  print "\n";
  foreach $warning (@warnings) {
    print "WARNING: $warning\n";
  }
}
