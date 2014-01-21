function CatalogCtrl($scope, $upload) {
  $scope.uploading = false
  $scope.upload = function(file) {
    $scope.uploading = true;
    $scope.upload = $upload.upload({
      url: '/api/modules/install',
      method: 'POST',
      file: file,
    }).progress(function(evt) {
      $scope.uploadProgress = parseInt(100.0 * evt.loaded / evt.total);
    }).success(function() {
      $scope.uploading = false;
      console.log('upload successful');
    }).error(function() {
      $scope.uploading = false;
      console.error('upload failed');
    });
  };
}
