angular.module('GHome').filter('truncate', function () {
  return function (text, length, end){
    if (text === undefined) {
      return;
    }

    // Default value for length
    if (isNaN(length)) { length = 10; }

    // Default value for end
    if (end === undefined) { end = '...'; }

    // Actual filter
    if (text.length <= length || text.length - end.length <= length) {
      return text;
    } else {
      return String(text).substring(0, length - end.length) + end;
    }
  };
});
