require 'rails_helper'

RSpec.describe ListsController, type: :controller do
  let(:user) { create(:user) }
  before { user.create_api_key }

  describe "GET #index" do
    before { 5.times { create :list, user: user } }

    context 'when wrong token' do
      subject { get :index, access_token: "wrong_token", format: :json }

      it "should return not authorized" do
        subject
      expect(json).to eq({ "status" => 403, "message" => "You are not authorized to access this resource"})
      end
    end

    context 'when correct token' do
      subject { get :index, access_token: user.access_token, page: 1, per_page: 2, format: :json }

      it { expect(response.status).to eq 200 }

      it 'should return lists from first page' do
        list = user.lists.first
        subject
        expect(json['lists']).to be_present
        expect(json['lists'].length).to eq 2
        expect(json).to include("lists_count" => 5)
        expect(json['lists'][0]).to include(
          {
              "id" => list.id,
              "user_id" => list.user_id,
              "name" => list.name,
              "identifier" => list.identifier,
              "created_at" => list.created_at.strftime("%FT%T.%3NZ"),
              "updated_at" => list.updated_at.strftime("%FT%T.%3NZ")
          })
      end

      it 'should return lists from second page' do
        get :index, access_token: user.access_token, page: 2, per_page: 2, format: :json
        list = List.third
        expect(json['lists'].length).to eq 2
        expect(json).to include("lists_count" => 5)
        expect(json['lists'][0]).to include(
          {
              "id" => list.id,
              "user_id" => list.user_id,
              "name" => list.name,
              "identifier" => list.identifier,
              "created_at" => list.created_at.strftime("%FT%T.%3NZ"),
              "updated_at" => list.updated_at.strftime("%FT%T.%3NZ")
          })
      end
    end
  end

  describe "GET #show" do
    let(:list) { create :list, user: user }
    let(:another_list) { create :list, user: create(:user) }

    it "should not show list when not authorized" do
      get :show, access_token: "wrong token", format: :json, id: list.id

      expect(json).to eq({ "status" => 403, "message" => "You are not authorized to access this resource"})

    end

    it "should not show other user's list when authorized" do
      get :show, access_token: user.access_token, format: :json, id: another_list.id

      expect(json).to eq({ "status" => 403, "message" => "You are not authorized to access this resource"})
    end

    it "should show user's list when authorized" do
      get :show, access_token: user.access_token, format: :json, id: list.id

      expect(json).to eq(
        {
          "list" => {
            "id" => list.id,
            "name" => list.name,
            "identifier" => list.identifier,
            "created_at" => list.created_at.strftime("%FT%T.%3NZ"),
            "updated_at" => list.updated_at.strftime("%FT%T.%3NZ"),
            "user_id" => user.id,
            "user" => {
              "id" => user.id,
              "created_at" => user.created_at.strftime("%FT%T.%3NZ"),
              "updated_at" => user.reload.updated_at.strftime("%FT%T.%3NZ"),
              "email" => user.email
            },
            "tasks" => []
            }
          })
    end
  end

  describe "POST #create"do
    context "with authorization" do

      it "creates a new list" do
        expect{ post :create, access_token: user.access_token, list: { name: 'test' }, format: :json
        }.to change(List, :count).by(1)
        list = List.last
        expect(list.name).to eq 'test'
        expect(list.user).to eq user
        expect(json).to eq({
          "list" => {
            "id" => list.id,
            "name" => list.name,
            "identifier" => list.identifier,
            "created_at" => list.created_at.strftime("%FT%T.%3NZ"),
            "updated_at" => list.updated_at.strftime("%FT%T.%3NZ"),
            "user_id" => user.id,
            "user" => {
              "id" => user.id,
              "created_at" => user.created_at.strftime("%FT%T.%3NZ"),
              "updated_at" => user.reload.updated_at.strftime("%FT%T.%3NZ"),
              "email" => user.email
            },
            "tasks" => []
            }
          })
      end
    end

    it "should not create list when not authorized" do
      expect{post :create, access_token: "wrong_token", list: { name: 'Test'}, format: :json}.not_to change{List.count}

      expect(json).to eq({ "status" => 403, "message" => "You are not authorized to access this resource"})

    end
  end
end

