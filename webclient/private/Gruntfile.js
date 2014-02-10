var path = require('path');

module.exports = function(grunt) {
  // Directories and files
  var dirs = { src: '.', dest: '../public' }, files = {
    js: {
      all: [path.join(dirs.src, 'js', '**/*.js')],
      dist: path.join(dirs.dest, 'js', 'main.js')
    }, less: {
      all: [path.join(dirs.src, 'less', '**/*.less')],
      src: [path.join(dirs.src, 'less', 'main.less')],
      dist: path.join(dirs.dest, 'css', 'main.css')
    }
  };

  grunt.initConfig({
    pkg: grunt.file.readJSON(path.join(__dirname, 'package.json')),
    concat: {
      options: {
        separator: ';'
      }, dist: {
        src: files.js.all,
        dest: files.js.dist
      }
    }, uglify: {
      options: {
        mangle: false
      }, dist: {
        files: (function() {
          var ret = {};
          ret[files.js.dist] = files.js.dist;
          return ret;
        })()
      }
    }, less: {
      dist: {
        options: {
          yuicompress: true
        }, files: (function() {
          var ret = {};
          ret[files.less.dist] = files.less.src;
          return ret;
        })()
      }
    }, watch: {
      js: {
        files: files.js.all,
        tasks: ['concat'],
        interrupt: true
      }, less: {
        files: files.less.all,
        tasks: ['less'],
        interrupt: true
      }
    }
  });

  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-contrib-concat');
  grunt.loadNpmTasks('grunt-contrib-less');
  grunt.loadNpmTasks('grunt-contrib-watch');

  grunt.registerTask('default', ['concat', 'uglify', 'less']);
  grunt.registerTask('dev', ['default', 'watch']);
};
