# ==========================================
# CONFIGURACIÓN DE TU NUEVA SECUENCIA
# ==========================================
pasos_config = [
    {"numero": 10, "tiempo_ms": 1000, "comentario": "PASO 10: Inicialización del sistema."},
    {"numero": 20, "tiempo_ms": 1500, "comentario": "PASO 20: Reset de módulos de seguridad."},
    {"numero": 30, "tiempo_ms": 2000, "comentario": "PASO 30: Habilitación de drives activos."}
]

# ==========================================
# GENERADOR CON CABECERA V38.01 ENCONTRADA
# ==========================================
def generar_archivo_l5x(lista_pasos, nombre_archivo="Rutina_Secuencia_Generada.L5X"):
    # Usamos tu cabecera exacta de Studio 5000 v38.01
    xml = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    xml += '<RSLogix5000Content SchemaVersion="1.0" SoftwareRevision="38.01" TargetName="R00_Principal" TargetType="Routine" TargetSubType="RLL" ContainsContext="true" Owner="Esau, SEI Automation" ExportDate="Fri May 29 12:27:50 2026" ExportOptions="References NoRawData L5KData DecoratedData Context Dependencies ForceProtectedEncoding AllProjDocTrans">\n'
    xml += '<Controller Use="Context" Name="Ruta_2104_REV_0">\n'
    xml += '  <Routines Use="Context">\n'
    xml += '    <Routine Use="Target" Name="R00_Principal" Type="RLL">\n'
    xml += '      <RLLContent>\n'
    
    rung_index = 0
    
    for i, paso in enumerate(lista_pasos):
        num = paso["numero"]
        tiempo = paso["tiempo_ms"]
        comentario = paso["comentario"]
        id_timer = i + 1
        
        # Generar Rung de activación de temporizador
        xml += f'        <Rung Number="{rung_index}" Type="N">\n'
        xml += f'          <Comment><![CDATA[###\n{comentario}\n###]]></Comment>\n'
        xml += f'          <Text><![CDATA[EQ(Sec_Inicial,{num})TON(TIEMPOS_SECC_INICIAL[{id_timer}],{tiempo},0);]]></Text>\n'
        xml += '        </Rung>\n'
        rung_index += 1
        
        # Generar Rung de brinco al siguiente paso
        siguiente_paso = lista_pasos[i+1]["numero"] if i < len(lista_pasos)-1 else 0
        xml += f'        <Rung Number="{rung_index}" Type="N">\n'
        xml += f'          <Text><![CDATA[EQ(Sec_Inicial,{num})XIC(TIEMPOS_SECC_INICIAL[{id_timer}].DN)MOVE({siguiente_paso},Sec_Inicial);]]></Text>\n'
        xml += '        </Rung>\n'
        rung_index += 1

    # Cierre de la estructura respetando tu jerarquía XML
    xml += '      </RLLContent>\n'
    xml += '    </Routine>\n'
    xml += '  </Routines>\n'
    xml += '</Controller>\n'
    xml += '</RSLogix5000Content>\n'
    
    with open(nombre_archivo, "w", encoding="utf-8") as f:
        f.write(xml)
    
    print(f"¡Éxito! Archivo V38.01 generado en '{nombre_archivo}'.")

generar_archivo_l5x(pasos_config)
