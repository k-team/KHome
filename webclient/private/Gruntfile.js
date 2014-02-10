var path = require('path');

module.exports = function(grunt) {
  // Directories
  var dirs = {
    client: '.', build: 'build',
    public: '../public'
  };
  // ...files
  var files = {
    js: {
      all: [path.join(dirs.client, 'js', '**/*.js')],
      build: path.join(dirs.build, 'js', 'main.js'),
      dist: path.join(dirs.public, 'js', 'main.js')
    }, less: {
      all: [path.join(dirs.client, 'less', '**/*.less')],
      src: [path.join(dirs.client, 'less', 'main.less')],
      dist: path.join(dirs.public, 'css', 'main.css')
    }
  };

  grunt.initConfig({
    pkg: grunt.file.readJSON(path.join(__dirname, 'package.json')),
    clean: [dirs.public, dirs.build],
    concat: {
      options: {
        separator: ';'
      }, dist: {
        src: files.js.all,
        dest: files.js.build
      }
    }, uglify: {
      options: {
        mangle: false
      }, dist: {
        files: (function() {
          var ret = {};
          ret[files.js.dist] = files.js.build;
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
        tasks: ['concat', 'uglify'],
        interrupt: true
      }, less: {
        files: files.less.all,
        tasks: ['less'],
        interrupt: true
      }
    }
  });

  grunt.loadNpmTasks('grunt-contrib-clean');
  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-contrib-concat');
  grunt.loadNpmTasks('grunt-contrib-less');
  grunt.loadNpmTasks('grunt-contrib-watch');

  grunt.registerTask('default', ['concat', 'uglify', 'less']);
  grunt.registerTask('dev', ['default', 'watch']);
};
