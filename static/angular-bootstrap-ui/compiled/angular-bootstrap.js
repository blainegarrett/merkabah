// Generated by CoffeeScript 1.3.3
(function() {

  angular.module('angularBootstrap', ['angularBootstrap.modal', 'angularBootstrap.tabs', 'angularBootstrap.popover']);

  /*
  modal. Restrict class. Options:
  	ng-model (scope-variable, optional, default=none)
  	  If ng-model is NOT set, this will behave like a normal
  	  bootstrap modal, except backdrop/keyboard options will be used
  	  If ng-model IS set, the value will be set to true whenever the
  	  modal is open, and false when it is closed.
  	  Additionally, you may set it to true to open the
  	  modal and set it to false to close it.
  	backdrop: (boolean, optional, default=true)
  	  Decides whether the modal has a backdrop when opening
  	keyboard: (boolean, optional, default=true)
  	  Decides whether the modal can be closed with escape key	
  
  Example usage, showing both ways of opening/closing the modal:
  <div id="myModal" class="modal hide" ng-model="modalVariable">
  	<button ng-click="modalVariable = false">Close Modal</button>
  </div>
  <a href="#myModal" data-toggle="modal">Open Modal</a>
  */


  angular.module('angularBootstrap.modal', []).directive('modal', [
    '$timeout', function($timeout) {
      var $;
      $ = jQuery;
      return {
        restrict: 'C',
        require: '?ngModel',
        scope: true,
        link: function(scope, elm, attrs, model) {
          $(elm).modal({
            backdrop: scope.backdrop,
            keyboard: scope.keyboard,
            show: false
          });
          if (model == null) {
            return;
          }
          scope.$watch(attrs.ngModel, function(value) {
            if (value === true) {
              return $(elm).modal('show');
            } else {
              return $(elm).modal('hide');
            }
          });
          $(elm).bind('shown', function() {
            return $timeout(function() {
              return scope.ngModel(true);
            });
          });
          return $(elm).bind('hidden', function() {
            return $timeout(function() {
              return scope.ngModel(false);
            });
          });
        }
      };
    }
  ]);

  angular.module('angularBootstrap.popover', []).directive('strapPopover', [
    function() {
      var $, defaults, getBounds, linkFn;
      $ = jQuery;
      defaults = {
        placement: 'right',
        margin: 0
      };
      getBounds = function($el) {
        return $.extend($el.offset(), {
          width: $el[0].offsetWidth || $el.width(),
          height: $el[0].offsetHeight || $el.height()
        });
      };
      linkFn = function(scope, elm, attrs) {
        var $this, currentSource, directiveOptions, hidePopover, showPopover, togglePopover;
        $this = $(elm).hide().addClass('popover');
        directiveOptions = {
          placement: attrs.placement
        };
        currentSource = null;
        showPopover = function(options) {
          var $source, decidePosition, margin, placement, popBounds, sourceBounds;
          $source = options.$source, placement = options.placement, margin = options.margin;
          if ($source === currentSource) {
            return;
          }
          popBounds = getBounds($this);
          sourceBounds = getBounds($source);
          decidePosition = function() {
            switch (placement) {
              case 'inside':
                return {
                  top: sourceBounds.top,
                  left: sourceBounds.left
                };
              case 'left':
                return {
                  top: sourceBounds.top + sourceBounds.height / 2 - popBounds.height / 2,
                  left: sourceBounds.left - popBounds.width - margin
                };
              case 'top':
                return {
                  top: sourceBounds.top - popBounds.height - margin,
                  left: sourceBounds.left + sourceBounds.width / 2 - popBounds.width / 2
                };
              case 'right':
                return {
                  top: sourceBounds.top + sourceBounds.height / 2 - popBounds.height / 2,
                  left: sourceBounds.left + sourceBounds.width + margin
                };
              case 'bottom':
                return {
                  top: sourceBounds.top + sourceBounds.height + margin,
                  left: sourceBounds.left + sourceBounds.width / 2 - popBounds.width / 2
                };
            }
          };
          $this.css(decidePosition()).fadeIn(250);
          return currentSource = $source;
        };
        hidePopover = function() {
          $this.fadeOut(250);
          return currentSource = null;
        };
        togglePopover = function(options) {
          if ($this.css('display') === 'none') {
            return showPopover(options);
          } else {
            return hidePopover();
          }
        };
        return $this.bind('popoverShow', function(evt, eventOptions) {
          return showPopover($.extend(defaults, directiveOptions, eventOptions));
        }).bind('popoverHide', function() {
          return hidePopover();
        }).bind('popoverToggle', function(evt, eventOptions) {
          return togglePopover($.extend(defaults, directiveOptions, eventOptions));
        });
      };
      return {
        restrict: 'E',
        scope: {
          title: '='
        },
        link: linkFn,
        transclude: true,
        template: "<div class=\"arrow\"></div>\n<div class=\"popover-inner\">\n	<h3 class=\"popover-title\">{{title}}</h3>\n	<div class=\"popover-content\" ng-transclude></div>\n</div>"
      };
    }
  ]).directive('popTarget', [
    function() {
      var $, linkFn;
      $ = jQuery;
      linkFn = function(scope, elm, attrs) {
        var $popover, $this, bindPopoverEvent, setPopoverOpenCloseEvents;
        $popover = $(attrs.popTarget);
        $this = $(elm);
        bindPopoverEvent = function(sourceEventType, popoverEventType, callback) {
          return $this.bind(sourceEventType, function() {
            if (typeof callback === "function") {
              callback();
            }
            return $popover.trigger(popoverEventType, [
              {
                $source: $this,
                placement: attrs.popPlacement,
                eventType: attrs.popEvent,
                margin: parseInt(attrs.popMargin || '0')
              }
            ]);
          });
        };
        setPopoverOpenCloseEvents = {
          hover: function() {
            return bindPopoverEvent('mouseover', 'popoverShow', function() {
              var mouseInCount, onMouseout, onMouseover;
              mouseInCount = 1;
              onMouseover = function() {
                return mouseInCount++;
              };
              onMouseout = function() {
                mouseInCount--;
                return setTimeout(function() {
                  if (mouseInCount === 0) {
                    $popover.trigger('popoverHide');
                    $this.unbind('mouseover', onMouseover).unbind('mouseout', onMouseout);
                    return $popover.unbind('mouseover', onMouseover).unbind('mouseout', onMouseout);
                  }
                }, 150);
              };
              $this.bind('mouseover', onMouseover).bind('mouseout', onMouseout);
              return $popover.bind('mouseover', onMouseover).bind('mouseout', onMouseout);
            });
          },
          focus: function() {
            bindPopoverEvent('focus', 'popoverShow');
            return bindPopoverEvent('blur', 'popoverHide');
          },
          click: function() {
            return bindPopoverEvent('click', 'popoverToggle');
          }
        };
        if (attrs.popEvent != null) {
          return setPopoverOpenCloseEvents[attrs.popEvent]();
        }
      };
      return {
        restrict: 'A',
        link: linkFn
      };
    }
  ]);

  /*
  strap-tabs
  Example usage:
  <strap-tabs>
  	<strap-tab title="Hello">Content</strap-tab>
  	<strap-tab title="getTitle()"><h1>I love things!</h1></strap-tab>
  	<div ng-repeat="stuff in things">
  		<strap-tab title="{{stuff}}">{{stuff.things}}</strap-tab>
  	</div>
  </strap-tabs>
  */


  angular.module('angularBootstrap.tabs', []).directive('strapTabs', [
    '$timeout', function($timeout) {
      var controllerFn;
      controllerFn = function($scope, $element, $attrs) {
        $scope.tabs = [];
        $scope.$watch('tabs.length', function(tabsL, oldL) {
          if (tabsL > 0 && tabsL < oldL) {
            if ($scope.tabs.indexOf($scope.selectedTab === -1)) {
              return $scope.selectTab($scope.tabs[Math.max($scope.selectedIdx - 1, 0)]);
            }
          }
        });
        $scope.selectTab = function(tab) {
          var _i, _len, _ref, _tab;
          _ref = $scope.tabs;
          for (_i = 0, _len = _ref.length; _i < _len; _i++) {
            _tab = _ref[_i];
            _tab.selected(false);
          }
          tab.selected(true);
          $scope.selectedTab = tab;
          return $scope.selectedIdx = $scope.tabs.indexOf(tab);
        };
        this.addTab = function(tab, index) {
          $scope.tabs.push(tab);
          if ($scope.tabs.length === 1) {
            return $scope.selectTab(tab);
          }
        };
        return this.removeTab = function(tab) {
          return $timeout(function() {
            return $scope.tabs.splice($scope.tabs.indexOf(tab, 1));
          });
        };
      };
      return {
        restrict: 'E',
        transclude: true,
        controller: controllerFn,
        template: "<div class=\"tabbable\">\n	<ul class=\"nav nav-tabs\">\n		<li ng-repeat=\"tab in tabs\" ng-class=\"{active: tab.selected()}\">\n			<a href=\"\" ng-click=\"selectTab(tab)\">{{tab.title}}</a>\n		</li>\n	</ul>\n	<div class=\"tab-content\" ng-transclude>\n	</div>\n</div>"
      };
    }
  ]).directive('strapTab', [
    function() {
      var linkFn, nextTab;
      nextTab = 0;
      linkFn = function(scope, elm, attrs, container) {
        var tab;
        tab = {
          title: scope.title,
          selected: function(newVal) {
            if (newVal == null) {
              return scope.selected;
            }
            return scope.selected = newVal;
          }
        };
        container.addTab(tab);
        return scope.$on('$destroy', function() {
          return container.removeTab(tab);
        });
      };
      return {
        restrict: 'E',
        transclude: true,
        require: '^strapTabs',
        link: linkFn,
        scope: {
          title: '='
        },
        template: "<div class=\"tab-pane\" ng-class=\"{active:selected}\" ng-show=\"selected\" ng-transclude></div>"
      };
    }
  ]);

}).call(this);