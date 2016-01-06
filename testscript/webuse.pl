#!/usr/bin/perl

my $version = 1.5;

my $iconbase = "avatars/";
my $namesfile = "names.txt";
my $sentence_file = "sentences.txt";
my $imagefile = "images.txt";
my $tempdir = "/run/shm/";

use Data::Dumper;
# use MongoDB;
# use MongoDB::MongoClient;
# use MongoDB::OID;
use Time::HiRes;
use Sys::Hostname;

use Getopt::Std;
getopts( "q:U:upcfr:v", \my %opt ) or die "wrong parameters\n";


my $weburl = $opt{'U'} if $opt{'U'};

my $VERBOSE = $opt{'v'};

sub verbose {
    print $_[0] if $VERBOSE;
}

verbose("Url: http://$weburl\n");

newUser() if $opt{'u'};

newPost() if $opt{'p'};

newComment() if $opt{'c'};

frontPage() if $opt{'f'};



if ( $opt{r} ){
	print "random algorithm: $opt{r}\n";

	( $user, $post, $comment, $front ) = split /:/,$opt{r};
	$sum = $user + $post + $comment + $front;
	verbose("weight (user/post/comment/front): $user / $post / $comment / $front, sum: $sum\n");
	$rand = int(rand($sum));
	verbose("random number: $rand\n");
	if ( $rand <= $user ){
		verbose("creating user\n");
		newUser();		
	} elsif ( $rand <= ( $post + $user ) ){
		verbose("adding post\n");
		newPost();
	} elsif ( $rand <= ( $post + $user + $comment ) ) {
		verbose("commenting\n");
		newComment();		
	} else {
		verbose("viewing frontpage\n");
		frontPage();		
	}
	
	
}

sub frontPage {
	
	$rand = int(rand(1000));
    print "TASK: frontpage\n";
	verbose("random number: $rand\n");
	system("mkdir $tempdir$rand");
	system("cd $tempdir$rand; wget -t 2 -T 5 -p -q http://$weburl/index.php");
	system("rm -r $tempdir$rand");
}

sub newPost {
	print "TASK: new post\n";
	open(HOME,"wget -O - -q -t 2 -T 5 http://$weburl/index.php |");
	# download "homepage"
	while( my $line = <HOME> ){
#		print "$line";
		if ( $line =~ /Users:.*>(\d+)<\/td>/ ){
			verbose("Total users: $1\n");
			$user = int(rand($1));
			print "POST BY: $user\n";
				# find a userID
			return if $user == 0;	
			    # download users homepage
		        my $rand = int(rand(1000));
		        system("mkdir $tempdir$rand");
			system("cd $tempdir$rand; wget -t 2 -T 5 -p -q http://$weburl/showuser.php?user=$user");
			system("rm -r $tempdir$rand");
			
				# generate text

				my $alt_text = getRandomSentence();
				$alt_text =~ s/'//g;
				$alt_text =~ s/\(.*\)//g;
				use URI::Escape;
				$encode = uri_escape($alt_text);
				verbose("'$text'\n");
				verbose("'$encode'\n");				
			$url = "wget -t 2 -T 5 -O - -q http://$weburl/addpost.php?user=$user\\&post=$encode";
			print "URL: $url\n";
			system("$url");
			
		}
	}

			

	

	
	# post text
	
}

sub getRandomSentence {
	$limit = 2200;
	open(SEN,$sentence_file); 
        if ( not SEN ){
	    return "Error open file: $!";
	}
	my $linenum = int(rand($limit));
	for ($i = 0; $i < $linenum; $i++){
		<SEN>;
	}
	$line = <SEN>;
	close(SEN);
	chomp $line;
	return $line;
}

sub newComment {
    
    print "TASK: new comment\n";
    
	# download "homepage"
	
	# find a userID
	
	# download users homepage
	
	# find a postID
	
	# generate text
	
	# post text	

	open(HOME,"wget -t 2 -T 5 -O - -q http://$weburl/index.php |");
	# download "homepage"
	while( my $line = <HOME> ){
#		print "$line";
		if ( $line =~ /Users:.*>(\d+)<\/td>/ ){
			verbose("Total users: $1\n");
			$user = int(rand($1));
			$commenter = int(rand($1));
			
			print "Picking user $user\n";
				# find a userID
				
			    # download users homepage
		    my $rand = int(rand(1000));
		    system("mkdir $tempdir$rand");
			system("cd $tempdir$rand; wget -t 2 -T 5 -nd  -p -q http://$weburl/showuser.php?user=$user");

			open(PAGE,"$tempdir$rand/showuser.php?user=$user") or die "failed to open file: $tempdir$rand/showuser.php?user=$user $!";
			my $postcount; 
			while($line = <PAGE> ){
				if ( $line =~ /posts: (\d+)</ ){
					$postcount = $1;
					last;
				}
			}
			verbose("postcount: $postcount\n");
			my $postitem = int(rand($postcount)) + 1;
			print "picking postnumber $postitem\n";
			my $newcount = 1;
			my $targetPostID;
			while ( $line = <PAGE>){
				if ( $line =~ /postID:(\d+) /  ){
					if ( $newcount == $postitem ){
						verbose("will comment on postID $1\n");
						$targetPostID = $1;
						last;
					}	
				    $newcount++;	
				}
			}
			close(PAGE);
			
			system("rm -r $tempdir$rand");
			
			if ( not $targetPostID ){
				exit 0;
			}	
				# generate text
				my $alt_text = getRandomSentence();
				$alt_text =~ s/'//g;
				$alt_text =~ s/\(.*\)//g;
				use URI::Escape;
				$encode = uri_escape($alt_text);
			
				verbose("'$encode'\n");
			
			$url = "wget -t 2 -T 5 -O /dev/null -q http://$weburl/addcomment.php?user=$commenter\\&postID=$targetPostID\\&comment=$encode";
			print "URL: $url\n";
			system("$url");
			
		}
	}

	
}


sub newUser {

    print "TASK: new user\n";
# pick random name
$newname = getRandomName();
print "New name: $newname\n";
$newname =~ s/ /%20/g;
# ping random avatar
# open(FILES,$imagefile);
# @files = <FILES>;
# close(FILES);
# print "number of files " . $#files . "\n";
# $pictnum = int(rand(($#files + 1)));
# $newpict = $files[$pictnum];
# chomp($newpict);
# $newpict =~ s/\/.*\/(.*\.png)/$1/g;

    $avatar = getRandomAvatar();

# print "Picking $pictnum: $newpict\n";
# use URI::Escape;
my $url = "http://$weburl/newuser.php?user=$newname\\&image=$avatar";

print "URL: " . $url . "\n";
system("wget -t 2 -T 5 -O - -q $url");

}

sub getRandomAvatar {
    open(AVA,"wget -q -O - http://www.avatarsdb.com | ") or die "FATAL: $!\n";
    
    # Random Avatar
    while ( my $line = <AVA> ){
	if ( $line =~ "Random Avatar" ){
	    $line = <AVA>;
	    verbose("line: " . $line);
	    $line =~ s/^.*src=\"(.*(gif|jpeg|jpg)).*$/$1/;
	    $url = "http://www.avatarsdb.com/$line";
	    print "AVATAR: $url\n";
	    close AVA;
	    return $url; 
	}    
    }
    
}

sub getRandomName {
 
    
    open(NAME,"wget -O - -q 'https://randomuser.me/api/' | ") or die "AAAAh $!\n";
                                                                                                                                                  
    while( $line = <NAME> ){                                                                                                                    
	 # "first": "kim",
	 #                      "last": "murray"
	if ( $line =~ /first\": \"(.*)\"/ ){                                                                                                         
	    $firstname = $1;                                                                                                                    
	    $line = <NAME>;                                                                                                                     
	    $line =~ /last\": \"(.*)\"/;
	    my $lastname = $1;
	    chomp($line);
	    close(NAME); 
	    return "$firstname $lastname";                                                                                                         
	}                                                                                                                                       
	
    }                                                                                                                                           
    close(NAME); 
    
}
