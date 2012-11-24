
fs = require 'fs'
{spawn} = require 'child_process'

option '-w', '--watch', '(coffee task only) watch and re-run on file changes'

task 'coffee', 'compile source files in src/ to compiled/', (options) ->
	args = []
	args.push '-w' if options.watch
	args.push '-j', 'angular-bootstrap.js'
	args.push '-o', 'compiled/', '-c', 'src/'

	coffee = spawn 'coffee' , args
	coffee.stderr.on 'data', (data) ->
		console.error data.toString()
	coffee.stdout.on 'data', (data) ->
		console.log data.toString()

task 'build', 'concat compiled files for commit', ->

	# Add file with dependences in with 
	contents = []
	for file in fs.readdirSync 'lib/' 
		contents.push fs.readFileSync 'lib/'+file
	fs.writeFileSync 'compiled/angular-bootstrap-scripts.js', contents.join '\n\n'

	# Write the 'standalone' file (not really standalone, just doesn't need the bootstrap scripts)
	contents.unshift fs.readFileSync 'compiled/angular-bootstrap.js'
	fs.writeFileSync 'compiled/angular-bootstrap-with-scripts.js', contents.join '\n\n'
