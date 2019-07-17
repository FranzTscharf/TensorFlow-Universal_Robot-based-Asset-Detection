#!/usr/bin/perl -w

@files = <*.xml>;
foreach $file (@files) {
  open(F,$file);
  @list=<F>;close F;
  $this="<name>3AE53";
  @f=grep /$this/,@list;
  if (@f == ""){
  	print "no - del\n";
  	unlink $file;
  	$file =~s/.xml//;
	  $file =~ s!/*$!.jpg!;
	  unlink $file;
    $file =~s/.jpg//;
    $file =~ s!/*$!.JPG!;
    unlink $file;
  } else {
    print @f;
  }
}