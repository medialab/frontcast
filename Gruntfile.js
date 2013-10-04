module.exports = function(grunt) {
  grunt.initConfig({
    uglify: {
      options: {
        banner: '/*\n\n    Frontcast for FORCCAST Front-End \n    ================================\n\n*/\n'
      },
      prod: {
        files: {
          './static/js/build/frontcast.min.js': []
        }
      }
    }
  });

  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.registerTask('default', ['uglify']);
};
