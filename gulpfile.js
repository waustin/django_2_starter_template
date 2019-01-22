"use strict";

var gulp = require('gulp');
var gutil = require('gulp-util');
var sass = require('gulp-sass');
var watch = require('gulp-watch');
var autoprefixer = require('gulp-autoprefixer');
var minifycss = require('gulp-minify-css');
var sourcemaps = require('gulp-sourcemaps');
var uglify = require('gulp-uglify');
var pixrem = require('gulp-pixrem');
var imagemin = require('gulp-imagemin');
var plumber = require('gulp-plumber');
var notify = require('gulp-notify');

// Directories
var sourcemaps_dir = '../maps'
var sass_dir = 'assets/sass/**/*.scss'
var css_dir = 'assets/css/'
var image_dir = 'assets/images/**/*.*'
var js_dir = 'assets/js/'

var autoprefixerOptions = {
  browsers: ['last 2 versions', '> 5%', 'Firefox ESR']
};

var onError = function(err) {
    notify.onError({
      title:    "Gulp error in " + err.plugin,
      message:  err.toString()
    })(err);
    this.emit('end');
}

// Compress Images
gulp.task('imagemin', function() {
    gulp.src(image_dir)
        .pipe(imagemin())
        .pipe(gulp.dest('assets/images'))  // Write to same directory as source. This seems to work
});

// Compile SASS
gulp.task('sass', function() {
    gulp.src(sass_dir)
        .pipe(plumber({
            errorHandler: onError
        }))
        .pipe(sourcemaps.init())
        .pipe(sass().on('error', sass.logError))
        .pipe(autoprefixer(autoprefixerOptions))
        .pipe(pixrem())  // add fallbacks for rem units
        .pipe(minifycss())
        .pipe(sourcemaps.write(sourcemaps_dir))
        .pipe(gulp.dest(css_dir))
});
// Watch
gulp.task('watch', function() {
    gulp.watch(sass_dir, ['sass'])
    .on('change', function(event) {
        console.log('File ' + event.path + ' was ' + event.type + ', running tasks...');
    });
});

gulp.task('default', ['sass', 'watch']);
