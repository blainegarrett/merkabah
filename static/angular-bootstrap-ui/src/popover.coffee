angular.module('angularBootstrap.popover', [])
.directive('strapPopover', [ ->
	$ = jQuery

	defaults =
		placement: 'right'
		margin: 0

	# gets bounds for an element. i
	# if offsetWidth or offsetHeight are 0, take .width() and .height() instead
	getBounds = ($el) -> 
		$.extend $el.offset(),
			width: $el[0].offsetWidth or $el.width()
			height: $el[0].offsetHeight or $el.height()

	linkFn = (scope, elm, attrs) ->
		$this = $(elm).hide().addClass 'popover'

		directiveOptions =
			placement: attrs.placement

		currentSource = null

		showPopover = (options) ->
			# source = guy we're popping over
			{$source, placement, margin} = options

			# no need to re-popover if this is the same source as the one we're currently on
			return if $source is currentSource

			popBounds = getBounds $this
			sourceBounds = getBounds $source

			decidePosition = -> 
				switch placement
					when 'inside'
						top: sourceBounds.top
						left: sourceBounds.left
					when 'left'
						top: sourceBounds.top + sourceBounds.height/2 - popBounds.height/2
						left: sourceBounds.left - popBounds.width - margin
					when 'top'
						top: sourceBounds.top - popBounds.height - margin
						left: sourceBounds.left + sourceBounds.width/2 - popBounds.width/2
					when 'right'
						top: sourceBounds.top + sourceBounds.height/2 - popBounds.height/2
						left: sourceBounds.left + sourceBounds.width + margin
					when 'bottom'
						top: sourceBounds.top + sourceBounds.height + margin
						left: sourceBounds.left + sourceBounds.width/2 - popBounds.width/2

			$this.css( decidePosition() ).fadeIn 250
			currentSource = $source

		hidePopover = ->
			$this.fadeOut 250
			currentSource = null

		togglePopover = (options) ->
			if $this.css('display') is 'none'
				showPopover options
			else
				hidePopover()

		$this.bind('popoverShow', (evt, eventOptions) ->
			showPopover($.extend defaults, directiveOptions, eventOptions)
		)
		.bind('popoverHide', ->
			hidePopover()
		)
		.bind('popoverToggle', (evt, eventOptions) ->
			togglePopover($.extend defaults, directiveOptions, eventOptions)
		)

	return {
		restrict: 'E'
		scope:
			title: '='
		link: linkFn
		transclude: true
		template: """
		<div class="arrow"></div>
		<div class="popover-inner">
			<h3 class="popover-title">{{title}}</h3>
			<div class="popover-content" ng-transclude></div>
		</div>
		"""
	}
])
.directive('popTarget', [ ->
	$ = jQuery

	linkFn = (scope, elm, attrs) ->
		$popover = $(attrs.popTarget)
		$this = $(elm)

		bindPopoverEvent = (sourceEventType, popoverEventType, callback) -> 
			$this.bind sourceEventType, ->
				callback?()
				$popover.trigger popoverEventType, [
					$source: $this
					placement: attrs.popPlacement
					eventType: attrs.popEvent
					margin: parseInt(attrs.popMargin or '0')
				]

		setPopoverOpenCloseEvents =
			hover: ->
				bindPopoverEvent 'mouseover', 'popoverShow', ->
					## Hide the popover if neither the source nor the popover are hovered
					# We do this by keeping track of whether the mouse is in popover or source,
					# using a count.  When it enters either source or popover, the count goes up.
					# When it leaves, the count goes down.  If count is 0, hide popover
					mouseInCount = 1 #starts at 1 because mouse is inside already
					onMouseover = -> mouseInCount++
					onMouseout = -> 
						mouseInCount--
						# set a timeout because the mosue may take a sec to move between the elements
						setTimeout ->
							# If mouse isn't in source or popover, hide popover
							if mouseInCount is 0
								$popover.trigger 'popoverHide' 
								$this.unbind('mouseover', onMouseover).unbind('mouseout', onMouseout)
								$popover.unbind('mouseover', onMouseover).unbind('mouseout', onMouseout)
						, 150

					$this.bind('mouseover', onMouseover).bind('mouseout', onMouseout)
					$popover.bind('mouseover', onMouseover).bind('mouseout', onMouseout)

			focus: ->
				bindPopoverEvent 'focus', 'popoverShow'
				bindPopoverEvent 'blur', 'popoverHide'

			click: ->
				bindPopoverEvent 'click', 'popoverToggle'

		setPopoverOpenCloseEvents[attrs.popEvent]() if attrs.popEvent?
			

	return {
		restrict: 'A'
		link: linkFn
	}
])