
import os
from . import  bpThesis
from werkzeug.utils import secure_filename
from urllib.parse import quote
from flask_login import  login_required, current_user
from flask import abort, render_template, current_app, flash, redirect, url_for, send_from_directory
from playhouse.flask_utils import get_object_or_404
from .forms_upload_file import UploadMaterialsForm
from .. models import Thesis
from ..constants import CntThesisMaterials

_all_ = ['uploadMaterials']


@bpThesis.route('/upload/materrials/<category>/<int:thesisId>', methods=['GET', 'POST'])
@login_required
def uploadMaterials(category, thesisId):
    thesis = get_object_or_404(Thesis, (Thesis.id == thesisId))
    me = current_user

    if thesis.teacher_id != me.id:
        abort(403)

    if category not in CntThesisMaterials.labels:
        abort(404)

    filePath = os.path.join(current_app.config['APP_THESIS_FOLDER'],
                            thesis.getFolderPath(me.chineseName))

    form = UploadMaterialsForm()
    if form.validate_on_submit():
        fName = u'untitled'
        fExtension = u'unknown'
        secureFileName = secure_filename(form.materials.data.filename)
        if secureFileName:
            res = secureFileName.rsplit('.', 1)
            if len(res) == 2:
                fName = res[0]
                fExtension = res[1]
            else:
                fName = ''
                fExtension = res[0]

        newFileInfo = None
        idx1 = 1
        oldFileInfo = getattr(thesis, category)
        if oldFileInfo is None:
            newFileInfo = u'{:02d}|{}'.format(1, fExtension)
        else:
            idx, _ = oldFileInfo.split(u'|')
            idx1 = int(idx) + 1
            newFileInfo = u'{:02d}|{}'.format(idx1, fExtension)

        pattern = thesis.getMaterialNamePattern(category)
        fileName = pattern.format(idx=idx1, ext=fExtension)
        form.materials.data.save(os.path.join(filePath, fileName))

        tplFileName = thesis.getTplMaterialName(category)
        if os.path.isfile(os.path.join(filePath, tplFileName)):
            os.remove(os.path.join(filePath, tplFileName))

        params = dict(zip([category], [newFileInfo]))
        query = Thesis.update(**params).where(Thesis.id == thesis.id)
        query.execute()

        flash(u'资料上传成功', 'success')
        return redirect(url_for('bpThesis.taught'))



    return render_template('thesis/teacher/uploadMaterials.html', form=form, category=category, thesis=thesis)

@bpThesis.route('/download/materials/<category>/<int:thesisId>', methods=['GET'])
@login_required
def downloadMaterials(category, thesisId):
    thesis = get_object_or_404(Thesis, (Thesis.id == thesisId))
    teacher = thesis.teacher
    me = current_user

    if category not in CntThesisMaterials.labels:
        abort(404)

    canDownload = False
    if thesis.teacher_id == me.id:
        canDownload = True

    idx1 = 0
    ext = u'unknown'
    fileInfo = getattr(thesis, category)
    if fileInfo is None:
        abort(404)
    else:
        idx, ext = fileInfo.split(u'|')
        idx1 = int(idx)

    pattern = thesis.getMaterialNamePattern(category)
    fileName = pattern.format(idx=idx1, ext=ext)
    encodeFileName = quote(fileName.encode('UTF-8'))
    filePath = os.path.join(current_app.config['APP_THESIS_FOLDER'],
                            thesis.getFolderPath(me.chineseName))

    return send_from_directory(filePath, fileName,
                               as_attachment=True,
                               attachment_filename=encodeFileName)