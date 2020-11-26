source 'https://rubygems.org'
git_source(:github) { |repo| "https://github.com/#{repo}.git" }

ruby '2.6.6'

# MANUALLY ADDED GEMS

# For authentication and authorization
gem 'devise', '4.7.3'
# For secrets
gem 'figaro'
# To improve code quality on controller responses
gem 'responders'
# Rubocop from terminal, to use run: rubocop, from the terminal. Your IDE might have rubocop integrated too (which would
# show offenses directly in code)
gem 'rubocop', '~> 0.89.0', require: false, group: :development
# For image uploading and storage. It includes a minimal module of both MiniMagick and RMagick, so you don't have to
# install any of them to use them, it suffices with uncommenting the corresponding line in your uploader.
gem 'carrierwave', '~> 2.0'
# Solargraph provides a comprehensive suite of tools for Ruby programming: intellisense, diagnostics, inline documentation, and type checking.
gem 'solargraph', group: :development
# The 'ruby-debug-ide' gem provides the protocol to establish communication between the debugger engine (such as debase or ruby-debug-base) and IDEs (for example, RubyMine, Visual Studio Code, or Eclipse).
gem 'ruby-debug-ide', group: :development
# Debase is a fast implementation of the standard Ruby debugger debug.rb for Ruby 2.0. It is implemented by utilizing a new Ruby TracePoint class. The core component provides support that front-ends can build on. It provides breakpoint handling, bindings for stack frames among other things.
gem 'debase', group: :development

# DEFAULT RAIL-NEW COMMAND GEMS

# Bundle edge Rails instead: gem 'rails', github: 'rails/rails'
gem 'rails', '~> 6.0.3', '>= 6.0.3.3'
# Use sqlite3 as the database for Active Record
gem 'sqlite3', '~> 1.4'
# Use Puma as the app server
gem 'puma', '~> 4.1'
# Use SCSS for stylesheets
gem 'sass-rails', '>= 6'
# Transpile app-like JavaScript. Read more: https://github.com/rails/webpacker
gem 'webpacker', '~> 4.0'
# Turbolinks makes navigating your web application faster. Read more: https://github.com/turbolinks/turbolinks
gem 'turbolinks', '~> 5'
# Build JSON APIs with ease. Read more: https://github.com/rails/jbuilder
gem 'jbuilder', '~> 2.7'
# Use Redis adapter to run Action Cable in production
# gem 'redis', '~> 4.0'
# Use Active Model has_secure_password
# gem 'bcrypt', '~> 3.1.7'

# Use Active Storage variant
# gem 'image_processing', '~> 1.2'

# Reduces boot times through caching; required in config/boot.rb
gem 'bootsnap', '>= 1.4.2', require: false

group :development, :test do
  # Call 'byebug' anywhere in the code to stop execution and get a debugger console
  gem 'byebug', platforms: [:mri, :mingw, :x64_mingw]
end

group :development do
  # Access an interactive console on exception pages or by calling 'console' anywhere in the code.
  gem 'web-console', '>= 3.3.0'
end

group :test do
  # Adds support for Capybara system testing and selenium driver
  gem 'capybara', '>= 2.15'
  # Support for selenium tests
  gem 'selenium-webdriver'
  # Easy installation and use of web drivers to run system tests with browsers
  gem 'webdrivers'
end

# Windows does not include zoneinfo files, so bundle the tzinfo-data gem
gem 'tzinfo-data', platforms: [:mingw, :mswin, :x64_mingw, :jruby]
