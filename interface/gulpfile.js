'use strict';

// Dependencies
var gulp = require('gulp');
var nodemon = require('nodemon');
var livereload = require('gulp-livereload');

var htmlDir = "./public/client/*.html"
var jsDir = "./public/client/**/*.js"
var cssDir = "./public/client/css/*.css"


gulp.task('default', function (cb) {
    livereload.listen();
    gulp.watch(cssDir,function(){
      gulp.src(cssDir).pipe(livereload());
    })
    gulp.watch(jsDir,function(){
      gulp.src(jsDir).pipe(livereload());
    })
    gulp.watch(htmlDir,function(){
      gulp.src(htmlDir).pipe(livereload());
    })
    return nodemon({
    script: 'server.js && rs',
  })
  .on('restart', function(){
    console.log('restarted');
  })
});
