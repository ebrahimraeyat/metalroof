

__title__ = "MetalRoof Workbench"
__author__ = "Roknabadi"
__url__ = "https://www.freecadweb.org"


from pathlib import Path
import FreeCADGui
import MetalRoofTools

wb_icon_path = str(
    Path(MetalRoofTools.__file__).parent.absolute() / "resources" / "icons" / "metal_roof.png"
)


class MetalRoofWorkbench(FreeCADGui.Workbench):
    global wb_icon_path
    MenuText = "MetalRoof"
    ToolTip = "Create Building MetalRoof"
    Icon = wb_icon_path

    def Initialize(self):
        """This function is executed when FreeCAD starts"""
        import MetalRoofTools
        from pathlib import Path

        self.metalroof_commands = MetalRoofTools.MetalRoofCommands
        self.appendToolbar("MetalRoofCommands", self.metalroof_commands)


    def Activated(self):
        """This function is executed when the workbench is activated"""
        return

    def Deactivated(self):
        """This function is executed when the workbench is deactivated"""
        return

    def ContextMenu(self, recipient):
        """This is executed whenever the user right-clicks on screen"""
        # "recipient" will be either "view" or "tree"
        self.appendContextMenu("MetalRoofCommands", self.metalroof_commands)

    def GetClassName(self):
        # this function is mandatory if this is a full python workbench
        return "Gui::PythonWorkbench"


FreeCADGui.addWorkbench(MetalRoofWorkbench())
