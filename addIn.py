#Author-
#Description-

import adsk.core, adsk.fusion, traceback,math
import io

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        doc = app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
        design = app.activeProduct

        # Get the root component of the active design.
        rootComp = design.rootComponent

        # Create a new sketch on the xy plane.
        sketches = rootComp.sketches;
        xyPlane = rootComp.xYConstructionPlane
        sketch = sketches.add(xyPlane)

        # Draw two connected lines.
        lines = sketch.sketchCurves.sketchLines;
        # Get all components in the active design.
        product = app.activeProduct
        #design = adsk.fusion.Design.cast(product)
        title = 'Import Spline csv'
        if not design:
            ui.messageBox('No active Fusion design', title)
            return
        
        # dlg = ui.createFileDialog()
        # dlg.title = 'Open CSV File'
        # dlg.filter = 'Comma Separated Values (*.csv);;All Files (*.*)'
        # if dlg.showOpen() != adsk.core.DialogResults.DialogOK :
        #     return
        
        # filename = dlg.filename
        matrix = []
        CSV_FILE = '/Users/rishimalhotra/Downloads/TOC_Coordinates.csv'
        f = open(CSV_FILE,'r')

        #print(matrix)
        # with open(CSV_FILE, 'r', encoding='utf-8-sig') as f:
        for statement in f:
            x,y,z = statement.split(",")
            matrix.append([float(x),float(y),float(z)])

        numRows = len(matrix)
        for arrayPos in range(numRows-1):
            thisRow = matrix[arrayPos]
            nextRow = matrix[arrayPos+1]
            #ui.messageBox(thisRow[0],thisRow[1],thisRow[2]) 
            line1 = lines.addByTwoPoints(adsk.core.Point3D.create(thisRow[0],thisRow[1],thisRow[2]), adsk.core.Point3D.create(nextRow[0],nextRow[1],nextRow[2]))
            # line1 = lines.addByTwoPoints(adsk.core.Point3D.create(0,0,0), adsk.core.Point3D.create(2,2,0))
        YSHIFT=.15
        lines.addByTwoPoints(adsk.core.Point3D.create(nextRow[0],nextRow[1],nextRow[2]),adsk.core.Point3D.create(nextRow[0],nextRow[1]+YSHIFT,nextRow[2]))
        for arrayPos in range(numRows-1,0,-1):
            thisRow = matrix[arrayPos]
            nextRow = matrix[arrayPos-1]
            line1 = lines.addByTwoPoints(adsk.core.Point3D.create(thisRow[0],thisRow[1]+YSHIFT,thisRow[2]), adsk.core.Point3D.create(nextRow[0],nextRow[1]+YSHIFT,nextRow[2]))
        
        lines.addByTwoPoints(adsk.core.Point3D.create(nextRow[0],nextRow[1]+YSHIFT,nextRow[2]), adsk.core.Point3D.create(nextRow[0],nextRow[1],nextRow[2]))

        # Revolve
        # axisLine = lines.addByTwoPoints(adsk.core.Point3D.create(-1, -5, 0), adsk.core.Point3D.create(1, -5, 0))


        #the axis
        axisLine = lines.addByTwoPoints(adsk.core.Point3D.create(-50, 0, 0), adsk.core.Point3D.create(50, 0, 0))

        # Get the profile defined by the circle.
        prof = sketch.profiles.item(0)

        # Create an revolution input to be able to define the input needed for a revolution
        # while specifying the profile and that a new component is to be created
        revolves = rootComp.features.revolveFeatures
        revInput = revolves.createInput(prof, axisLine, adsk.fusion.FeatureOperations.NewComponentFeatureOperation)

        # Define that the extent is an angle of pi to get half of a torus.
        angle = adsk.core.ValueInput.createByReal(2*math.pi)
        revInput.setAngleExtent(False, angle)

        # Create the extrusion.
        ext = revolves.add(revInput)

        #ui.messageBox('k my ass')
        # if not revAxis:
        #     ui.messageBox("no axis")
        #     return False
        # else:
        #     ui.messageBox("axis found")
        #     return True
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

# def stop(context):
#     ui = None
#     try:
#         app = adsk.core.Application.get()
#         ui  = app.userInterface
#         ui.messageBox('Stop addin')

#     except:
#         if ui:
#             ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
