class Notifier < ActionMailer::Base

  def rim(rim)
    @recipients = 'hello@jmoore.me'
    @from = rim.email
    @subject = "New Rim Added: #{rim.description}"
    body :rim => rim
  end

  def hub(hub)
    @recipients = 'hello@jmoore.me'
    @from = hub.email
    @subject    = "New Hub Added: #{hub.description}"
    body :hub => hub
  end
end
