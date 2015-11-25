require 'rails_helper'

RSpec.describe TasksController, type: :controller do
  let(:user) { create(:user) }
  before { user.create_api_key }

  describe "GET #index" do
    let(:list) { create :list, user: user }
    before { 5.times { create :task, list: list } }

    context 'when wrong token' do
      subject { get :index, access_token: "wrong_token", format: :json, list_id: list.id }

      it "should return not authorized" do
        subject
      expect(json).to eq({ "status" => 403, "message" => "You are not authorized to access this resource"})
      end
    end

    context 'when correct token' do
      subject { get :index, access_token: user.access_token, format: :json, list_id: list.id }

      it { expect(response.status).to eq 200 }

      it 'should return list\'s tasks' do
        task = list.tasks.first
        subject
        expect(json['tasks']).to be_present
        expect(json['tasks'].length).to eq 5
        expect(json).to include("tasks_count" => 5)
        expect(json['tasks'][0]).to include(
          {
            "id" => task.id,
            "name" => task.name,
            "list_id" => task.list_id,
            "priority"=>1,
            "created_at" => task.created_at.strftime("%FT%T.%3NZ"),
            "updated_at" => task.updated_at.strftime("%FT%T.%3NZ"),
            "identifier" => task.identifier,
            "x"=>task.x,
            "y"=>task.y,
            "duration" => task.duration
          })
      end
    end
  end

  describe "GET #show" do
    let(:list) { create :list, user: user }
    let!(:task) {create :task, list: list }
    before { 4.times { create :task, list: list } }

    let(:another_task) { create :task, list: create(:list, user: create(:user)) }

    it "should not show task when not authorized" do
      get :show, access_token: "wrong token", format: :json, id: task.id, list_id: list.id

      expect(json).to eq({ "status" => 403, "message" => "You are not authorized to access this resource"})

    end

    it "should not show other user's task when authorized" do
      get :show, access_token: user.access_token, format: :json, id: another_task.id, list_id: another_task.list_id

      expect(json).to eq({ "status" => 403, "message" => "You are not authorized to access this resource"})
    end

    it "should show user's task when authorized" do
      get :show, access_token: user.access_token, format: :json, id: task.id, list_id: list.id
      expect(json).to eq(
        {
          "task" => {
            "id" => task.id,
            "name" => task.name,
            "list_id" => task.list_id,
            "priority"=>1,
            "created_at" => task.created_at.strftime("%FT%T.%3NZ"),
            "updated_at" => task.updated_at.strftime("%FT%T.%3NZ"),
            "identifier" => task.identifier,
            "x"=>task.x,
            "y"=>task.y,
            "duration" => task.duration,
            "list" => {
              "id"=>list.id,
              "name"=>list.name,
              "identifier"=>list.identifier,
              "created_at"=>list.created_at.strftime("%FT%T.%3NZ"),
              "updated_at"=>list.updated_at.strftime("%FT%T.%3NZ"),
              "user_id"=>list.user_id
            }
          }
        })
    end
  end

  describe "POST #create"do
    let(:list) { create :list, user: user }
    context "with authorization" do

      it "creates a new task" do
        expect{ post :create, access_token: user.access_token, list_id: list.id, task: { name: 'test', duration: 3 }, format: :json
        }.to change{list.reload.tasks.count}.by(1)
        task = list.tasks.last
        expect(task.name).to eq 'test'
        expect(task.duration).to eq 3
        expect(task.list).to eq list
        expect(json).to eq({
          "task" => {
            "id" => task.id,
            "name" => task.name,
            "list_id" => task.list_id,
            "priority"=>1,
            "created_at" => task.created_at.strftime("%FT%T.%3NZ"),
            "updated_at" => task.updated_at.strftime("%FT%T.%3NZ"),
            "identifier" => task.identifier,
            "x"=>task.x,
            "y"=>task.y,
            "duration" => task.duration,
            "list" => {
              "id"=>list.id,
              "name"=>list.name,
              "identifier"=>list.identifier,
              "created_at"=>list.created_at.strftime("%FT%T.%3NZ"),
              "updated_at"=>list.updated_at.strftime("%FT%T.%3NZ"),
              "user_id"=>list.user_id
            }
          }
        })
      end
    end

    it "should not create list when not authorized" do
      expect{post :create, access_token: "wrong_token", list_id: list.id, task: { name: 'Test', duration: 3}, format: :json}.not_to change{Task.count}

      expect(json).to eq({ "status" => 403, "message" => "You are not authorized to access this resource"})

    end
  end
end

