class Notifier < ActionMailer::Base

  def rim(rim)
    @recipients = 'james@freebiketools.org'
    @from = rim.email
    @subject = "New Rim Added: #{rim.description}"
    body :rim => rim
  end

  def hub(hub)
    @recipients = 'james@freebiketools.org'
    @from = hub.email
    @subject    = "New Hub Added: #{hub.description}"
    body :hub => hub
  end
end
