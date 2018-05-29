var gulp            = require('gulp'),
    sass            = require('gulp-sass'),
    browserSync     = require('browser-sync'),
    concat          = require('gulp-concat'),
    uglify          = require('gulp-uglify'),
    rename          = require('gulp-rename'),
    cssnano         = require('gulp-cssnano'),
    del             = require('del'),
    autoprefixer    = require('gulp-autoprefixer'),
    sourcemaps      = require('gulp-sourcemaps');

gulp.task('sass', function(){
    return gulp.src('app/sass/**/*.scss')
        .pipe(sourcemaps.init())
            .pipe(sass({outputStyle: 'expanded'}).on('error', sass.logError))
            .pipe(autoprefixer(['last 15 versions', '> 1%', 'ie 8', 'ie 7'], { cascade: false }))
        .pipe(sourcemaps.write('../css', {addComment: true}))
        .pipe(gulp.dest('app/css'))
        .pipe(browserSync.reload({stream: true}))
});

gulp.task('browser-sync', function() {
    browserSync({
        server: {
            baseDir: 'app'
        },
        notify: false
    });
});

gulp.task('scripts', function() {
    return gulp.src([
            'app/libs/jquery/dist/jquery.min.js',
            'app/libs/bootstrap/dist/js/bootstrap.js',
            'app/libs/owl.carousel/dist/owl.carousel.min.js',
            'app/libs/photobox/photobox/jquery.photobox.js',
            'app/libs/inputmask/dist/inputmask/inputmask.js',
            'app/libs/sweetalert2/dist/sweetalert2.all.min.js',
            'app/libs/plyr/dist/plyr.min.js',
            'app/libs/tippyjs/dist/tippy.all.js',
            'app/libs/typed.min.js'
        ])
        .pipe(concat('libs.min.js'))
        .pipe(uglify())
        .pipe(gulp.dest('app/js'));
});

gulp.task('css-libs', ['sass'], function() {
    return gulp.src('app/css/libs.css')
        .pipe(cssnano())
        .pipe(rename({suffix: '.min'}))
        .pipe(gulp.dest('app/css'));
});

gulp.task('watch', ['browser-sync', 'css-libs', 'scripts'], function() {
    gulp.watch('app/sass/**/*.scss', ['sass']);
    gulp.watch('app/*.html', browserSync.reload);
    gulp.watch('app/js/**/*.js', browserSync.reload);
});

// ----------------------Дефолтный таск gulp --------------------------------

gulp.task('default', ['watch']);