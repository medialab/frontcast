module.exports = function(grunt) {
  grunt.initConfig({
    uglify: {
      options: {
        banner: '/*\n\n    Frontcast for FORCCAST Front-End \n    ================================\n\n*/\n'
      },
      production: {
        files: {
          './static/dist/js/frontcast.min.js': [
            'static/libs/domino.min.js',
            'static/libs/handlebars.helpers.js',
            'static/libs/handlebars.runtime.js',
            'static/libs/crossroads.min.js',
            'static/libs/hasher.min.js',
            'static/libs/domino.min.js',
            'static/js/walt.templates.min.js',
            'static/js/walt.js',
            'static/js/walt.domino.js',
            'static/js/domino/*.js',
          ]
        }
      }
    },
    handlebars: {
      production: {
        options: {
          namespace: 'Handlebars.templates',
          processName: function(filePath) {
            return filePath.split("/").pop().split('.').shift();
          }
        },
        files: {
          'static/js/walt.templates.min.js' : ['static/js/partials/*.handlebars']
        }
      }
    }
  });

  console.log("\n                      *     .--.\n                           / /  `\n          +               | |\n                 '         \\ \\__,\n             *          +   '--'  *\n                 +   /\\\n    +              .'  '.   *\n           *      /======\\      +\n                 ;:.  _   ;\n                 |:. (_)  |\n                 |:.  _   |\n       +         |:. (_)  |          *\n                 ;:.      ;\n               .' \:.    /  `.\n              / .-'':._.'`-. \\\n              |/    /||\\    \\|\n        jgs _..--\"\"\"````\"\"\"--.._\n      _.-'``                    ``'-._\n    -'                                '-\n\n");
  console.log(grunt.cli.tasks.join(''));

  grunt.loadNpmTasks('grunt-contrib-handlebars');
  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-contrib-less');

  grunt.registerTask('default', ['handlebars:production']);
  grunt.registerTask('production', ['handlebars:production', 'uglify:production']);

};
