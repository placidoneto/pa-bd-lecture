package com.seuprojeto.resource;

import java.util.List;

import com.seuprojeto.DTO.AlunoDTO;
import com.seuprojeto.domain.Aluno;
import com.seuprojeto.mapper.AlunoMapper;
import com.seuprojeto.service.AlunoService;

import jakarta.inject.Inject;
import jakarta.transaction.Transactional;
import jakarta.ws.rs.Consumes;
import jakarta.ws.rs.DELETE;
import jakarta.ws.rs.GET;
import jakarta.ws.rs.NotFoundException;
import jakarta.ws.rs.POST;
import jakarta.ws.rs.PUT;
import jakarta.ws.rs.Path;
import jakarta.ws.rs.PathParam;
import jakarta.ws.rs.Produces;
import jakarta.ws.rs.core.MediaType;


@Path("/aluno")
@Produces(MediaType.APPLICATION_JSON)
@Consumes(MediaType.APPLICATION_JSON)
public class AlunoResource {

    @Inject
    AlunoService alunoService;

    @GET
    @Path("/lista")
    public List<Aluno> listAll() {
        return alunoService.listarAlunos();
    }

    @GET
    @Path("/ativos")
    public List<Aluno> listAtivos() {
        return alunoService.listarAlunosAtivos();
    }

    @GET
    @Path("/{id}")
    public AlunoDTO findById(@PathParam("id") Long id) {
        Aluno aluno = alunoService.buscarPorId(id);
        if (aluno == null) {
            throw new NotFoundException("Aluno não encontrado");
        }
        return AlunoMapper.toDTO(aluno);
    }

    @POST
    @Transactional
    public AlunoDTO create(AlunoDTO dto) {
        Aluno aluno = new Aluno();
        aluno.nome = dto.nome;
        aluno.email = dto.email;
        aluno.ativo = dto.ativo;

        alunoService.salvar(aluno);
        return AlunoMapper.toDTO(aluno);
    }

    @PUT
    @Path("/{id}")
    @Transactional
    public AlunoDTO update(@PathParam("id") Long id, AlunoDTO updated) {
        Aluno aluno = alunoService.buscarPorId(id);
        if (aluno == null) {
            throw new NotFoundException("Aluno não encontrado");
        }

        aluno.nome = updated.nome;
        aluno.email = updated.email;
        aluno.ativo = updated.ativo;

        return AlunoMapper.toDTO(aluno);
    }

    @DELETE
    @Path("/{id}")
    @Transactional
    public void delete(@PathParam("id") Long id) {
        boolean deleted = alunoService.remover(id);
        if (!deleted) {
            throw new NotFoundException("Aluno não encontrado");
        }
    }
}
