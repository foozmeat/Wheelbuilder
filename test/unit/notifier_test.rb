require File.dirname(__FILE__) + '/../test_helper'

class NotifierTest < Test::Unit::TestCase
  FIXTURES_PATH = File.dirname(__FILE__) + '/../fixtures'
  CHARSET = "utf-8"

  include ActionMailer::Quoting

  def setup
    ActionMailer::Base.delivery_method = :test
    ActionMailer::Base.perform_deliveries = true
    ActionMailer::Base.deliveries = []

    @expected = TMail::Mail.new
    @expected.set_content_type "text", "plain", { "charset" => CHARSET }
    @expected.mime_version = '1.0'
  end

  def test_rim
    @expected.subject = 'Notifier#rim'
    @expected.body    = read_fixture('rim')
    @expected.date    = Time.now

    assert_equal @expected.encoded, Notifier.create_rim(@expected.date).encoded
  end

  def test_hub
    @expected.subject = 'Notifier#hub'
    @expected.body    = read_fixture('hub')
    @expected.date    = Time.now

    assert_equal @expected.encoded, Notifier.create_hub(@expected.date).encoded
  end

  private
    def read_fixture(action)
      IO.readlines("#{FIXTURES_PATH}/notifier/#{action}")
    end

    def encode(subject)
      quoted_printable(subject, CHARSET)
    end
end
