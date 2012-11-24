# angular-bootstrap-ui

**This project is now deprecated.  I recommend using angular-ui -> http://github.com/angular-ui/**

Angular-ui doesn't have the tabs directive or the popover.  The popover may be moved later, but the tabs directive is unneeded (just ng-repeat tab title elements and tab content elements).

***

A set of [AngularJS](http://angularjs.org/) components to make easy use of [Twitter Bootstrap](http://twitter.github.com/bootstrap/) UI goodies.

Demo at [http://ajoslin.github.com/angular-bootstrap-ui](http://ajoslin.github.com/angular-bootstrap-ui)

Usage
-----

* Requires jQuery
* Drop js/angular-bootstrap-with-scripts.js into your project, or if you already have all the necessary bootstrap scripts just drop angular-bootstrap.js in.

Development
-----------

* Requires [coffeescript](http://coffeescript.org) to develop.  Get it with [node.js](http://nodejs.org) and npm, running `npm install -g coffee-script` to install.
* Run `cake` to see compile options
* Before you commit, be sure to run both `cake coffee` and `cake build`, so all the js files are proper.
* Tests? Who needs tests?  These are directives, good sir!  (yeah, yeah, yeah) 