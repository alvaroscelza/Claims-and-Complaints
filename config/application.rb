require_relative 'boot'

require 'rails/all'

# Require the gems listed in Gemfile, including any gems
# you've limited to :test, :development, or :production.
Bundler.require(*Rails.groups)

module ClaimsAndComplaints
  class Application < Rails::Application
    # Use the responders controller from the responders gem
    config.app_generators.scaffold_controller :responders_controller

    config.load_defaults 5.1

    config.action_mailer.delivery_method = :smtp
    config.action_mailer.smtp_settings = {
        address: 'smtp.gmail.com',
        port: 587,
        domain: 'gmail.com',
        user_name: Rails.application.secrets.gmail_account,
        password: Rails.application.secrets.gmail_account_password,
        authentication: 'plain',
        enable_starttls_auto: true
    }
  end
end
