#!/usr/bin/perl

use Getopt::Std;
use strict "vars";
use Data::Dumper;
use Time::HiRes;
use Sys::Hostname;
use JSON;

my $VERBOSE = 0;
my $DEBUG = 0;
my $REPORT_TEXT = "";
my $VERSION = "0.2.0";
my $opt_string = 'hn:';
my $OUTPUT = "";


getopts( "$opt_string", \my %opt ) or usage() and exit 1;

# print help message if -h is invoked
if ( $opt{'h'} ){
        usage();
        exit 0;
}

$VERBOSE = 1 if $opt{'v'};
$DEBUG = 1 if $opt{'d'};

run_on_leeshore($opt{"n"}) if $opt{"n"};

sub run_on_leeshore {
    my $name = $_[0];
    $REPORT_TEXT = "";

    my $tenant_name = $name;
    verbose("$name has tenant $tenant_name\n");
    my %report;

    $report{"name"} = $name;
    $report{"type"} = "leeshore";
    $report{"check_time"} = time;
    $report{"workerhost"} = hostname . "-$VERSION";
    
    # get tenant ID
    open(TENANT,"keystone tenant-get $tenant_name |") or die("failed to run keystone command: $!\n");
    my $tid;
    while(my $line = <TENANT>){
	if( $line =~ /\|\s+id\s+\|\s+(\S+)\s+/ ){
	    $tid = $1;
	    last;
	}
    }
    
    verbose("Tenant $tenant_name has id '$tid'\n");
    if ( not $tid ){
	$report{"result: no tenant id found"};
	verbose("No tenant id found, exiting\n");
	return;	
    }
    # get list of ACTIVE VMs for tenant
    open(VMS,"nova list --all-tenants --tenant $tid | grep ACTIVE |");
    my @vms;
    my %names;
    while(my $line = <VMS> ){
	if ( $line =~ /\|\s+(\S+)\s+\|\s+(\S+)\s+/ ){
	    my $name = $2;
	    my $id = $1;
	    if ( not $name =~ /safe/ ){
		verbose("Found candidate $name with id: $id\n");
		push(@vms,"$id");
		$names{$id} = $name;
	    }
	}
    }
    # pick a random number
    my $random = $vms[rand @vms];
    if ( $random ){
	verbose("Picking $random for a leeshore\n");
    
    # stop the active virtual machine
	$report{"result"} = "$names{$random} runs om a leeshore!";
# Enable this
	system("nova stop $random");
    } else {
	verbose("No candidate was found.");
	$report{"result"} = "No candidate was found";
    }
 #   $reports->insert(\%report);
    my $jsonstring = encode_json \%report;
    print $jsonstring;
}




sub verbose {
    print "VERBOSE: " . $_[0] if ( $VERBOSE or $DEBUG );
}

sub debug {
    print "DEBUG: " . $_[0] if ( $DEBUG );
}

sub usage {
    
    print "Usage: ./leeshore_short.pl options...\n";
}

sub out {

    if ( $OUTPUT ){
	print OUT $_[0];
    } else {
	print $_[0];   
	$REPORT_TEXT .= $_[0];
    }
}
