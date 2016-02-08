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
my $VERSION = "0.0.2";
my $opt_string = 'hvdn:';
my $OUTPUT = "";


getopts( "$opt_string", \my %opt ) or usage() and exit 1;

# print help message if -h is invoked
if ( $opt{'h'} ){
        usage();
        exit 0;
}

$VERBOSE = 1 if $opt{'v'};
$DEBUG = 1 if $opt{'d'};

clerk($opt{"n"}) if $opt{"n"};

sub clerk {
    my $name = $_[0];
    $REPORT_TEXT = "";

    my $tenant_name = $name;
    verbose("$name has tenant $tenant_name\n");
    my %report;

    open(FLAVORS,"nova flavor-list |") or die("failed to run keystone command: $!\n");
    my %flavors;
    while(my $line = <FLAVORS>){
	if( $line =~ /\|\s+(\S+)\s+\|\s+(\S+)\s+/ and not $line =~ /ID.*Name/){
	    verbose("Storing flavor $1 -> $2\n");
	    $flavors{$1} = $2;
	}
    }

    
    $report{"name"} = $name;
    $report{"type"} = "clerk";
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
    open(VMS,"nova list --all-tenants --tenant $tid --fields name,flavor --status active |");
    my @vms;
    my %vmcount;
    while(my $line = <VMS> ){
	if ( $line =~ /\|\s+(\S+)\s+\|\s+(\S+)\s+\|\s+(\S+)\s+/ and not $line =~ /ID.*Name/){
	    my $flavor = $3;
	    my $name = $2;
	    my $id = $1;
	    verbose("VM $name with id: $id, $name and flavor $flavor\n");
#		push(@vms,"$id");
	    $vmcount{$flavors{$3}} += 1;
	}
    }

    foreach my $key (keys %flavors){
	if( not $vmcount{$flavors{$key}} ){
	    $vmcount{$flavors{$key}} = 0;
	}
    }
    
    %{$report{"vmcount"}} = %vmcount;
    # pick a random number
    # $reports->insert(\%report);

    
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
