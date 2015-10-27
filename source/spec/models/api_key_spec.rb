require 'rails_helper'

RSpec.describe ApiKey, type: :model do
  let(:api_key) { ApiKey.new }

  before { api_key.send(:generate_access_token) }
  it { expect(api_key.access_token.size).to eq(32) }
end
