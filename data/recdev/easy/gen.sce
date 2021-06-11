// generate dataset
fname = unix_g('noext *.jpg');

for i=1:size(fname,'*')
  a = imread(fname(i) + '.jpg');
  b = a/2;
//  b = a + 2*(26/255)*(rand(a)-0.5);
//  b = normal(b);
  imwrite(b,fname(i) + '-dark.jpg');
end

//for i=1:size(fname,'*')
//  a = imread(fname(i) + '.jpg');
//  b = a + 2*(26/255)*(rand(a)-0.5);
//  b = normal(b);
//  imwrite(b,fname(i) + '-noise.jpg');
//end

// mogrify -resize 100x100 is done after the above has been performed on the
// 260x260
