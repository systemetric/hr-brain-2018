const gulp = require('gulp');
const zip = require('gulp-zip');
 
gulp.task('default', () =>
    gulp.src('src/*')
        .pipe(zip('code.zip'))
        .pipe(gulp.dest('dist'))
);

gulp.watch('src/*', ['default']); 
