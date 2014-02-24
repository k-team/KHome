function StoreCtrl($scope, ModuleService, $modal, $timeout) {
  // All modules
  $scope.availableModules = [];

  // Explicitly reload modules
  $scope.reloadAvailableModules = function() {
    $scope.loading = true;
    ModuleService.available().then(function(modules) {
      $scope.availableModules = modules;
      $scope.loading = false;
      $scope.unreachable = false;
    }, function() {
      $scope.loading = false;
      $scope.unreachable = true;
    });
  };
  //...and call immediately
  $scope.reloadAvailableModules();

  // Install a module
  $scope.modulesInstalling = [];
  $scope.removeInstallingModule = function(module) {
    for (var i = 0; i < $scope.modulesInstalling.length; i++) {
      if ($scope.modulesInstalling[i].name == module.name) {
        $timeout(function() { $scope.modulesInstalling.splice(i, 1) }, 1000);
        break;
      }
    }
  };

  $scope.moduleAlreadyInstalling = function(module) {
    for (var i = 0; i < $scope.modulesInstalling.length; i++) {
      if ($scope.modulesInstalling[i].name == module.name) {
        return;
      }
    }
  };

  $scope.install = function(module) {
    if ($scope.moduleAlreadyInstalling(module)) { return; }

    // Start installing
    $scope.modulesInstalling.push(module);
    ModuleService.installFromCatalog(module).then(function() {
      $scope.removeInstallingModule(module);
      module.installed = true;
    }, function() {
      $scope.removeInstallingModule(module);
    });
  };

  // Uploading system
  $scope.uploading = false
  $scope.upload = function(file) {
    $scope.uploading = true;
    $scope.upload = ModuleService.installFromFile(file).progress(function(evt) {
      $scope.uploadProgress = parseInt(100.0 * evt.loaded / evt.total);
    }).success(function() {
      $scope.uploading = false;
      $scope.reloadAvailableModules();
    }).error(function() {
      $scope.uploading = false; // TODO handle errors better
    });
  };

  $scope.modalInstances = {};
  $scope.openModal = function(module) {
    var modalScope = $scope.$new(true);

    // Dismiss the modal
    modalScope.dismiss = function() {
      $scope.modalInstances[module.name].dismiss();
    };

    // Install the module
    modalScope.install = function() {
      $scope.install(module);
      modalScope.dismiss();
    };

    // Uninstall the module
    modalScope.uninstall = function() {
      $scope.uninstall(module);
      modalScope.dismiss();
    };

    // Access the modal's module
    modalScope.module = module;

    // Open the modal
    $scope.modalInstances[module.name] = $modal.open({
      templateUrl: 'modal.html',
      scope: modalScope
    });

    $scope.$on('$destroy', function () {
      modalScope.dismiss();
    });
  };
}
