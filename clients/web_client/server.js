// Module base dependencies
var express = require('express'),
    path = require('path');

// Application instance
var app = express();

// Debug/release guards
var inDevelopment = (app.get('env') == 'development'),
    debugOnly = function(fn) {
  if (inDevelopment) { fn(); }
}, releaseOnly = function(fn) {
  if (!inDevelopment) { fn(); }
};

// Error handler in debug mode
debugOnly(function() {
  app.use(express.errorHandler());
});

// All environments
app.set('port', process.env.PORT || 3000);

// Static files
var staticFilesDir = path.join(__dirname, 'public');
app.use(express.static(staticFilesDir));

// Favicon
//var iconFile = path.join(staticFilesDir, 'img', 'favicon.ico');
//app.use(express.favicon(iconFile));

// Other configuration options
app.use(express.logger('dev'));
app.use(express.methodOverride());
app.use(app.router);

// Start server
var http = require('http'),
    server = http.createServer(app);

// Startup
server.listen(app.get('port'), function() {
  debugOnly(function() {
    var address = server.address();
    console.log('Server started at http://%s:%s\nPress Ctrl-C to stop',
      address.address, address.port);
  });
});

// Shutdown
var shutdown = function() {
  debugOnly(function() {
    console.log('Server shutting down');
  });
  server.close();
  process.exit();
};
process.on('SIGINT', shutdown);
// ...only in debug mode
debugOnly(function() {
  process.on('uncaughtException', function(err) {
    console.log('Uncaught exception: ' + err);
    shutdown();
  });
});

// vim: ft=javascript et sw=2 sts=2
