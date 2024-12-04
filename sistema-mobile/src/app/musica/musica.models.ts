export class Musica
{
    public id: number;
    public banda: string;
    public musica: string;
    public ano: number;
    public foto: string | undefined;
    public estilo: string;


    constructor() {
        this.id = 0;
        this.banda = '';
        this.musica = '';
        this.ano = 0;
        this.estilo = '';
    }
}
