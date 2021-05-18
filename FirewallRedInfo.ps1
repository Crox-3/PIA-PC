$perfilRed = Get-NetConnectionProfile
$opc = $args[0]

Switch ($opc){
    "Status" {
        $resultado = "El perfil del firewall se encuentra en modo " + $perfilRed.NetworkCategory
    }
    "Public" {
        if($perfilRed.NetworkCategory -eq "Public"){
            $resultado = "El perfil del firewall ya estaba en modo Publico."
        } else{
            Set-NetConnectionProfile -Name $perfilRed.Name -NetworkCategory Public
            $resultado = "Perfil cambiado de Privado a Publico."
        }
    }
    "Private" {
        if($perfilRed.NetworkCategory -eq "Private"){
            $resultado = "El perfil del firewall ya estaba en modo Privado."
        } else{
            Set-NetConnectionProfile -Name $perfilRed.Name -NetworkCategory Private
            $resultado = "Perfil cambiado de Publico a Privado."
        }
    }
    default {$resultado = "ERROR. Ingrese una opcion valida."}
}

Write-Host $resultado
