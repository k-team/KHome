function RatingCtrl($scope, ModuleService) {
  $scope.isRating = false;
  $scope.setRating = function(module, value) {
    $scope.isRating = true;
    ModuleService.rateModule(module, value).then(function() {
      console.log('rating success');
    }, function() {
      console.log('rating error');
    }, function() {
      $scope.isRating = false;
    });
  };
}

function StoreCtrl($scope, $modal, ModuleService) {
  // All modules
  $scope.modules = [];

  // Explicitly reload modules
  $scope.reloadModules = function() {
    ModuleService.available().then(function(modules) {
      $scope.modules = modules;
    });
  };
  //...and call immediately
  $scope.reloadModules();

  // Install a module
  $scope.install = function(module) {
    console.log('installing module', module);
  };

  // Uploading system
  $scope.uploading = false
  $scope.upload = function(file) {
    $scope.uploading = true;
    $scope.upload = ModuleService.install(file).progress(function(evt) {
      $scope.uploadProgress = parseInt(100.0 * evt.loaded / evt.total);
    }).success(function() {
      $scope.uploading = false;
      $scope.reloadModules();
    }).error(function() {
      $scope.uploading = false;
      // TODO handle errors better
    });
  };

  $scope.modalInstances = {};
  $scope.openModal = function(module) {
    var modalScope = $scope.$new(true);

    // Dismiss the modal
    modalScope.dismiss = function() {
      $scope.modalInstances[module.id].dismiss();
    };

    // Install the module
    modalScope.install = function() {
      $scope.install(module);
      modalScope.dismiss();
    };

    // Access the modal's module
    modalScope.module = module;

    // Open the modal
    $scope.modalInstances[module.id] = $modal.open({
      templateUrl: 'modal.html',
      scope: modalScope
    });
  };
}
