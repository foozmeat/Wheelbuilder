module SlidingSessions
  # Allows using :session_expires_after option for session cookies
  # NOTE it does not perform any checks on server-side, it just
  # sets the session cookie expiration time.
  # see http://wiki.rubyonrails.org/rails/pages/HowtoChangeSessionOptions
  # for a recipe to perform server-side expiration checks

  # (C) Paweł Stradomski , released under MIT licence
  def self.extended(base)
    class << base
      alias_method :session_options_for_without_sliding, :session_options_for
      alias_method :session_options_for, :session_options_for_with_sliding
    end
  end

  def session_options_for_with_sliding(request, action) #:nodoc:
    opts = session_options_for_without_sliding(request, action)
    if opts[:session_expires_after] then
      opts[:session_expires] = Time.now + opts[:session_expires_after]
    end
    opts
  end
end

ActionController::Base.extend(SlidingSessions)
