/*
Merkabah Angular Bindings
*/

var merkabahModule = angular.module('merkabah', ['ngResource', 'ngSanitize', 'angularBootstrap']);

merkabahModule.config(function($locationProvider){ $locationProvider.html5Mode(true).hashPrefix('!'); });


// Your controller's Routes Mapping
merkabahModule.config(function($routeProvider) {
        /* TODO : Eventually make these load via JS */
        
        //$routeProvider.when('/:merkabahURL', {template: 'asdf({{ message }}', controller:MainCtrl});
        
        var default_when_args = {template : '<div ng-bind-html-unsafe="message">zebras</div>', action: "load_from_server", controller:MainCtrl}
        
        //2012/11/18/the-day-the-world-stood-still
        
        $routeProvider.when('/:merkabahURL', default_when_args);
        $routeProvider.when('/:year/:month/:day/:slug', default_when_args);        
        
        //$routeProvider.otherwise({templateUrl: '/'})
        
        /*
        $routeProvider.
        when('/', {templateUrl: '/'}).
        when('/about/', {templateUrl: '/about/'}).
        when('/contact/', {templateUrl: '/contact/'}).
        when('/links/', {templateUrl: '/links/'}). //.
        when('/gallery/', {templateUrl: '/gallery/'}). //.
        when('/clients/', {templateUrl: '/clients/'}). //.
        otherwise({redirectTo:'/', templateUrl:'/'});
        */
});


//Demo.controller(
 //           "AppController",
 //           function( $scope, $route, $routeParams ){
                
function MainCtrl($route, $compile, $rootScope, $routeParams, $scope, $location, $http, $resource) {
    var merkabahURL = $location.$$url
    
    //console.log(merkabahURL)
    
    function render() {
        $scope.message = ''    
        
        if ($route.current.action == 'load_from_server'){
            
            url = merkabahURL + '?get_content=True';
            $http.get(url).success(function(data) {
                var template = angular.element(data.content)
                var linkFn = $compile(template);
                linkFn($scope);
                $scope.message = template
            }).error(function(data, status, headers, config){
                var template = angular.element('<h2>' + status + ' Error Loading Page</h2><p>Unable to load url ' + $route.current.pathParams.merkabahURL + '</p> ');
                var linkFn = $compile(template);
                linkFn($scope);
                $scope.message = template
                
            });
            
            return 
            stuff = $resource($route.current.pathParams.merkabahURL + '?get_content=True', {}, 
                { query: { method: 'get', isArray: false }}
            );
            stuff.query({}, function(response) {
                //$('#supercoolstuff').html(response.content)
                //$scope.message = response.content; 
                
                // From the angular docs http://docs.angularjs.org/guide/directive
                var template = angular.element(response.content)
                var linkFn = $compile(template);
                linkFn($scope);
                $scope.message = template
                
            });            
        }
    }
    
    $scope.$on("$routeChangeStart",
        function($event, $nextRoute, $currentRoute){
            /*
            if (!$currentRoute) {
                $event.preventDefault();                
                return false;
            }
            */           
        }
    );
    
    $scope.$on("$routeChangeSuccess",
        function( $currentRoute, $previousRoute, $location){
            // Update the rendering.
            render();
        }
    );
    
    $scope.$on('$routeChangeError', 
        function( $currentRoute, $previousRoute, $rejection){
            alert('boo')
        }
    );
     
    
    $scope.callAction = function(clickObj) {
         url = clickObj.srcElement.href
         $.ajax(url, 
             {
                 success : function(data, textStatus, jqXHR) {
                     alert(data);
                 }
             }
         )
        
    }
    $scope.setRoute = function(route){
        $location.path(route);
    }
    $scope.showTab = function(pos, $event){
        // pos is an int or 'next' or 'prev'
        $event.preventDefault();
        $event.stopPropagation();
        
        $('#myCarousel').carousel(pos)
        //$($event.target).tab('show');
        
        return false;
    } 
}

merkabahModule.directive('tooltip', function () {
    return {
        restrict:'A',
        link:function postLink(scope, element, attrs) {
            $(element).click(function(){
                alert('space butts');
            })
        }
    }
});

merkabahModule.directive('tooltip', function () {
    return {
        restrict:'A',
        link:function postLink(scope, element, attrs) {
            $(element).tooltip();
        }
    }
});

function RouteController($scope, xcontent) {
    $scope.xcontent = xcontent.data;
}
RouteController.resolve = {
    xcontent : function($http) {
        return $http({
            method: 'GET', 
            url: '/projects/'
        });
    }
};


(function($) {
    window.merkabah = {};
})(jQuery);
