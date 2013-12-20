var path = require('path');

module.exports = function(grunt) {
  // Directories
  var dirs = {
    client: 'static',
    public: 'public',
    build: 'build'
  };
  // ...files
  var files = {
    html: { index: path.join(dirs.public, 'index.html') },
    js: {
      src: path.join(dirs.build, 'js', 'main.js'),
      dest: path.join(dirs.public, 'js', 'main.js')
    },
    jade: { index: path.join(dirs.client, 'index.jade') },
    coffee: { src: path.join(dirs.client, '**', '*.coffee'), }
  };

  grunt.initConfig({
    pkg: grunt.file.readJSON(path.join(__dirname, 'package.json')),
    clean: [dirs.public, dirs.build],
    coffee: {
      compile: {
        options: {
          join: true
        },
        expand: true,
        flatten: true,
        src: [files.coffee.src],
        dest: files.js.src,
        ext: '.js'
      }
    }, uglify: {
      options: {
        mangle: false
      }, dist: {
        files: (function() {
          var ret = {};
          ret[files.js.dest] = path.join(files.js.src, '*.js');
          return ret;
        })()
      }
    }, jade: {
      dist: {
        files: (function() {
          var ret = {};
          ret[files.html.index] = files.jade.index;
          return ret;
        })()
      }
    }, watch: {
      coffee: {
        files: files.coffee.src,
        tasks: ['coffee', 'uglify'],
        interrupt: true
      }, jade: {
        files: [files.jade.index],
        tasks: ['jade']
      }
    }
  });

  grunt.loadNpmTasks('grunt-contrib-clean');
  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-contrib-coffee');
  grunt.loadNpmTasks('grunt-contrib-jade');

  grunt.registerTask('default', ['clean', 'coffee', 'uglify', 'jade']);

  // Development only
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.registerTask('dev', 'Run the development server', function() {
    grunt.task.run('default');
    grunt.util.spawn({
      cmd: 'npm',
      args: ['start'],
      opts: {
        stdio: ['pipe', process.stdout, process.stderr]
      }
    });
    grunt.task.run('watch');
  });
};
