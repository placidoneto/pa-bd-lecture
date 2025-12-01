package  com.seuprojeto.DTO;
import java.time.LocalDate;

public class BeneficioAlunoDTO {
    public Long id;
    public String observacao;
    public LocalDate data_concessao;
    public Boolean ativo;
    public Long alunoId;
    public Long auxilioId;
}
