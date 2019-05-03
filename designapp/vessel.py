import math
from decimal import *
# The try should be done with liquid_flux=100, vapor_flux=975, liquid_density=1000, vapor_density=75, API=30

def process(liquid_flux, vapor_flux, liquid_density, vapor_density, API):
    liquid = liquid_flux # Liquid_flux
    vapor = vapor_flux # Vapor_flux
    dl = liquid_density # Liquid_density
    dg = vapor_density # Vapor_density
    API = API # API
    K = 0
    A = 0
    AG = 0
    VG = 0
    QG = 0
    F = 0
    DI = 0
    Dnozzle = 0
    VL = 0
    ANBBL_NAAL = 0
    QL = 0
    hL = 0
    tH = 0
    L = 2.25
    L_DI = 2.5
    hg = 0.3
    hg_D = 0.5
    Vr1 = 0
    Vr2 = 0
    Vnozzle = 0
    Vertical = False
    orientation = "Horizontal"

    R1 = liquid / (vapor + liquid) # Relationship of liquid-feed flux
    R2 = liquid / vapor # Relationship of feed liquid-vapor flux

    # Selection of the vessel orientation
    if R1 < 0.6:
        Vertical = True
    else:
        Vertical = False

    if Vertical == True:
        # Selection of K
        if R2 <= 0.1:
            K = 0.35
        elif 0.1 < R2 < 1:
            K = 0.25
        elif R2 >= 1:
            K = 0.2

        # Selection of the cross-sectional area
        VG = K * math.sqrt((dl - dg)/ dg)
        QG = vapor / dg
        A = Decimal(QG) / Decimal(VG) # Cross-sectional area A(m^2)
        Ap = A * Decimal(math.pow(3.2808, 2)) # Cross sectional area Ap(ft^2)

        # Selection of the internal diameter
        DI = math.sqrt(Decimal(4) * A / Decimal(3.1416))

        # Liquid Flux(lt/min*ft^2)
        F = (liquid / dl) * 60 * 1000 * (1 / Ap)

        # Mixture density
        dm = (liquid + vapor) / (liquid / dl + vapor / dg)

        # Nozzle velocity
        Vnozzle = 80 / math.sqrt(dm)

        Dnozzle = math.sqrt(Decimal(4) * (liquid / dl + vapor / dg) / (Decimal(3.1416) * Decimal(Vnozzle)))
    else:
        Vertical = False

    if (Vertical == True):
        # Retention time
        if API >= 40:
            tH = 1.5
        elif 25 <= API < 40:
            tH = 3
        elif 0 < API < 25:
            tH = 5

        # Height selection
        QL = liquid / dl # Liquid volumetric flux

        Vr1 = 60 * QL * tH # Operation volume
        hL = Vr1 / A # Liquid height

        # Low-low liquid level
        NBBL = Decimal(0.23)

        # Emergency retention volume
        Vr2 = QL * 600

        # NBBL_NAAL height
        NBBL_NAAL = hL + Vr2 / A

        # Bottom_NAAL height
        bottom_NAAL = NBBL + NBBL_NAAL

        # NAAL_nozzle height
        NAAL_nozzle = Dnozzle

        # Nozzle_mesh height
        nozzle_mesh = 0.61

        # Selection of the nozzle_mesh that is greater
        if (nozzle_mesh < 0.5 * DI):
            nozzle_mesh = 0.5 * DI

        # Thickness of the mesh
        emesh = 0.15

        # Height from mesh to nozzle of vapor outlet
        h0 = 0.4

        # Selection of the height from mesh to nozzle of vapor outlet
        if (h0 < 0.15 * DI):
            h0 = 0.15 * DI

        # Nozzle_tangent height
        nozzle_tangent = nozzle_mesh + emesh + h0

        # Height of bottom tangent to upper tangent or effective height
        L = Decimal(bottom_NAAL) + Decimal(NAAL_nozzle) + Decimal(Dnozzle) + Decimal(nozzle_tangent)

        # Relationship L/DI
        L_DI = L / Decimal(DI)

        if (L_DI > 6):
            Vertical = False
    else:
        Vertical = False
        while(True):
            # Selection of K
            if 2.5 <= L_DI < 4:
                K = 0.4
            elif 4 <= L_DI <= 6:
                K = 0.5
            elif 6 < L_DI:
                K = 0.5 * (L_DI / 6) * 0.05

            VG = K * math.sqrt((dl - dg) / dg) # Design gas velocity

            QG = vapor / dg # Volumetric gas flux

            AG = Decimal(QG) / Decimal(VG) # The gas space of the transversal-sectional area

            QL = liquid / dl # Volumetric liquid flux

            Vr1 = Decimal(QL) * Decimal(tH) # Operational liquid retention volume

            Vr2 = QL * 600 # Liquid retention volume due the operators response time

            Vr = Vr1 + Decimal(Vr2) # Maximum liquid retention volume

            DI = Decimal(hg) / Decimal(hg_D) # Internal diameter

            while(True):

                L = Decimal(L_DI) * DI # Effective length

                ANBBL_NAAL = Vr / L # Liquid height

                A = (Decimal(3.1416) / 4) * Decimal(math.pow(DI,2)) # Total vessel transversal area

                NBBL = Decimal(0.23) # Liquid low-low level

                angle = 2 * math.acos(1 - 2 * NBBL / DI) # String angle

                Aabottom_NBBL = (Decimal(angle) - Decimal(math.sin(angle))) / (2 * Decimal(3.1416)) # Bottom liquid cross-sectional area fraction about the liquid total area

                Abottom_NBBL = A * Aabottom_NBBL # Liquid cross-sectional area from bottom to NBBL

                AVD = A - (Abottom_NBBL + ANBBL_NAAL) # Vapor cross-sectional area

                if (AVD - AG) / AG <= 0.001:
                    break
                else:
                    DI = DI + 0.001

            AaG = AVD / A # Vapor cross-sectional area fraction
            angleG = Decimal(0.001) # Initial seed for the vapor cross-sectional angle

            while(True):
                AaGs = (Decimal(angleG) - Decimal(math.sin(angleG))) / (2 * Decimal(3.1416))
                if (AaGs - AaG) / AaG > 0.001:
                    angleG = angleG + 0.001
                else:
                    break
            hg_D = Decimal(0.5) * (1 - Decimal(math.cos(angleG / 2))) # Relationship hg / D

            if hg_D < 20:
                if DI * Decimal(0.2) < Decimal(0.3):
                    hg = Decimal(0.3)
                    hg_D = hg / DI
                else:
                    hg = Decimal(0.2) * DI

            if 2.5 <= L_DI <= 6:
                break
            else:
                L = L + 0.75

    if (Vertical == True):
        orientation = "Vertical"
    else:
        orientation = "Horizontal"

    vessel_height = L
    vessel_diameter = DI
    vessel_L_D = L_DI

    return vessel_height, vessel_diameter, vessel_L_D, orientation, Vnozzle, F, K
