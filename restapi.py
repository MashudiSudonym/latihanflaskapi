from flask import Flask, jsonify, request, abort
from flask_restful import Resource, Api, reqparse
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5432/postgres"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
api = Api(app)

class Datanama(db.Model):
	__tablename__ = "datanama"

	equip_id = db.Column(db.Integer, unique=True, primary_key=True)
	nama = db.Column(db.String(100))
	alamat = db.Column(db.String(254))

	def __init__(self, nama, alamat):
		self.nama = nama
		self.alamat = alamat

	def __repr__(self):
		return '<Datanama : %d>' % self.equip_id

class TugasApiList(Resource):
	def get(self):
		semuadata = Datanama.query.all()
		semuadata_all = []

		for data in semuadata:
			semuadata_all.append(
					[
						data.equip_id,
						data.nama,
						data.alamat,
					]
				)

		return jsonify({'data_nama': semuadata_all})

	def post(self):
		nama = request.get_json()['nama']
		alamat = request.get_json()['alamat']

		semuadata = Datanama(nama=nama, alamat=alamat)

		try:
			db.session.add(semuadata)
			db.session.commit()
		except:
			db.session.rollback()
			db.session.flush()

		semuanamaId = semuadata.equip_id
		data = Datanama.query.filter_by(equip_id=semuanamaId).first()

		hasil = [data.nama, data.alamat]
		return jsonify({'data_nama': hasil})

class TugasApi(Resource):
	def get(self, datanamaId):
		semuadata = Datanama.query.filter_by(equip_id=datanamaId)
		semuadata_byId = []

		for data in semuadata:
			semuadata_byId.append(
					[
						data.equip_id,
						data.nama,
						data.alamat,
					]
				)

		if len(semuadata_byId) == 0:
			abort(404)

		return jsonify({'data_nama': semuadata_byId})

	def put(self, datanamaId):
		data = Datanama.query.filter_by(equip_id=datanamaId).first()

		try:
			data.nama = request.get_json()['nama']
			data.alamat = request.get_json()['alamat']
			db.session.commit()
		except:
			db.session.rollback()
			db.session.flush()

		semuanamaId = data.equip_id
		dataSemua = Datanama.query.filter_by(equip_id=semuanamaId).first()

		hasil = [dataSemua.nama, dataSemua.alamat]
		return jsonify({'data_nama': hasil})

	def delete(self, datanamaId):
		data = Datanama.query.filter_by(equip_id=datanamaId).first()
		db.session.delete(data)
		db.session.commit()

		return "Data terhapus"

api.add_resource(TugasApiList, '/api')
api.add_resource(TugasApi, '/api/<int:datanamaId>')

if __name__ == '__main__':
	app.run(debug=True)