console.log('Inside Merkabah');

angular.module('merkabah', []).
    config(function($routeProvider) {
        $routeProvider.
            when('/about', {templateUrl: '/about'}).
            when('/stuff', {templateUrl: '/stuff'}).
            otherwise({redirectTo:'/', templateUrl:'/'});
    })
    .config(function($locationProvider){
        $locationProvider.html5Mode(true).hashPrefix('!');
    });


function MainCtrl($scope, $location, $http) {
    $scope.setRoute = function(route){
        console.log($location)
        $location.path(route);
    }
    
    $scope.get_json_result = function(route){
        console.log('hi..')
        
        $http.get('json_thing').success(function(data){
            console.log(data)
            //$('body').addClass(data['page_class'])
            //$('#main-content').html(data['rendered_content'])
        });        
    }   
}