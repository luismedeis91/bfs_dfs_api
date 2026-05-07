import os
from src.services.bairros_network import load_bairros_network, analyze_bairros_network, format_route_output

def main():
    data_path = os.path.join("data", "bairros_networks.json")
    
    if not os.path.exists(data_path):
        print(f"Erro: Arquivo {data_path} não encontrado.")
        return
        
    network = load_bairros_network(data_path)
    
    origem = "Centro"
    destino = "Papicu"
    
    print(f"Sistema de Planejamento de Rotas (Fortaleza)")
    print(f"Buscando rota de {origem} para {destino}...")
    
    resultado = analyze_bairros_network(network, origem, destino)
    
    print("\n" + format_route_output(resultado))
    
    print("\nOutro exemplo")
    origem2 = "Benfica"
    destino2 = "Varjota"
    print(f"Buscando rota de {origem2} para {destino2}...")
    resultado2 = analyze_bairros_network(network, origem2, destino2)
    print(format_route_output(resultado2))

if __name__ == "__main__":
    main()
