# L01 - Fundamentos SQL em PostgreSQL

### O que é o SQL?

O Angular é um framework para construir aplicações cliente em HTML, CSS e JavaScript/TypeScript. Ele utiliza a abordagem de SPA (**_Single Page Application_**), permitindo que a aplicação seja carregada uma vez e, em seguida, as mudanças de conteúdo ocorram dinamicamente sem recarregar a página.

### Por que usar o Angular?

- **Produtividade**: O Angular fornece ferramentas e estruturas que facilitam o desenvolvimento ágil e eficiente.
- **Arquitetura sólida**: Seu design modular e orientado a componentes simplifica a organização do código e a reutilização de funcionalidades.
- **Performance**: O Angular otimiza o desempenho da aplicação, garantindo uma experiência rápida e fluida para os usuários.
- **Ecossistema e comunidade ativa**: A plataforma Angular possui uma grande comunidade de desenvolvedores e uma vasta quantidade de bibliotecas e recursos disponíveis.

### Principais características e benefícios

- **TypeScript**: O Angular é escrito em TypeScript, que adiciona recursos de tipagem estática ao JavaScript, tornando o código mais robusto e legível.
- **Data Binding**: O poderoso mecanismo de data binding facilita a sincronização dos dados entre os componentes e o template.
- **Injeção de Dependência**: O Angular possui um sistema de injeção de dependência que permite gerenciar as dependências entre os componentes de forma eficiente.
- **Diretivas**: As diretivas permitem estender a sintaxe HTML, criando comportamentos personalizados para os elementos da página.
- **Roteamento**: O roteador do Angular permite criar aplicações de várias páginas dentro de uma SPA, gerenciando as transições entre os componentes.
- **Testabilidade**: O Angular incentiva práticas de teste, tornando as aplicações mais confiáveis e fáceis de manter.

### Arquitetura do Angular

A arquitetura do Angular é baseada em alguns conceitos fundamentais, como **_componentes_**, **_módulos_**, **_serviços_** e **_diretivas_**. Esses elementos são combinados para criar uma estrutura sólida e modular para desenvolver aplicações web com eficiência e escalabilidade.

1. **Componentes**:

Os componentes são blocos de construção essenciais do Angular. Eles são responsáveis por controlar partes específicas da interface do usuário e podem ser reutilizados em diferentes partes da aplicação. Cada componente possui um template associado que define a estrutura do DOM a ser renderizada.

Exemplo de um componente Angular:

```typescript
import { Component } from '@angular/core';

@Component({
  selector: 'app-exemplo', // Seletor do componente, usado para inserir o componente no template.
  templateUrl: './exemplo.component.html', // Caminho do template associado ao componente.
  styleUrls: ['./exemplo.component.scss'] // Arquivos de estilo associados ao componente.
})
export class ExemploComponent {
  // Lógica do componente aqui...
}
```