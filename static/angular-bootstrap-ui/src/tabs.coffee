
###
strap-tabs
Example usage:
<strap-tabs>
	<strap-tab title="Hello">Content</strap-tab>
	<strap-tab title="getTitle()"><h1>I love things!</h1></strap-tab>
	<div ng-repeat="stuff in things">
		<strap-tab title="{{stuff}}">{{stuff.things}}</strap-tab>
	</div>
</strap-tabs>
###
angular.module('angularBootstrap.tabs', [])
.directive('strapTabs', [ '$timeout', ($timeout) ->

	controllerFn = ($scope, $element, $attrs) ->
		$scope.tabs = []

		# Change selection when tabs are added/removed
		$scope.$watch 'tabs.length', (tabsL, oldL) ->
			# A tab was removed
			if tabsL > 0 and tabsL < oldL
				# If selected tab was removed
				if $scope.tabs.indexOf $scope.selectedTab is -1
					# select a new tab
					$scope.selectTab $scope.tabs[Math.max $scope.selectedIdx-1,0]

		$scope.selectTab = (tab) ->
			_tab.selected false for _tab in $scope.tabs 
			tab.selected true
			$scope.selectedTab = tab
			$scope.selectedIdx = $scope.tabs.indexOf tab

		# Uses `this` to be exposed for angularBootstrap-tab directive
		this.addTab = (tab, index) ->
			$scope.tabs.push tab
			# Select the tab if it's the only one in the array
			$scope.selectTab tab if $scope.tabs.length is 1

		this.removeTab = (tab) ->
			# Without the timeout, angular doesn't always catch this
			$timeout ->
				$scope.tabs.splice $scope.tabs.indexOf tab, 1

	return {
		restrict: 'E'
		transclude: true 
		controller: controllerFn
		template: """
		<div class="tabbable">
			<ul class="nav nav-tabs">
				<li ng-repeat="tab in tabs" ng-class="{active: tab.selected()}">
					<a href="" ng-click="selectTab(tab)">{{tab.title}}</a>
				</li>
			</ul>
			<div class="tab-content" ng-transclude>
			</div>
		</div>"""
	}
])
.directive('strapTab', [ ->
	nextTab = 0
	linkFn = (scope, elm, attrs, container) ->
		tab =
			title: scope.title
			selected: (newVal) ->
				return scope.selected unless newVal?
				scope.selected = newVal

		container.addTab tab

		scope.$on '$destroy', ->
			container.removeTab tab

	return {
		restrict: 'E'
		transclude: true
		require: '^strapTabs'
		link: linkFn
		scope:
			title: '='
		template: """
		<div class="tab-pane" ng-class="{active:selected}" ng-show="selected" ng-transclude></div>
		"""
	}
])