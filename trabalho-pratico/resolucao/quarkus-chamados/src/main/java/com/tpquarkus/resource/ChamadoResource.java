package com.tpquarkus.resource;

import java.util.List;

import com.tpquarkus.DTO.ChamadoDTO;
import com.tpquarkus.StatusChamado;
import com.tpquarkus.service.ChamadoService;

import jakarta.inject.Inject;
import jakarta.ws.rs.Consumes;
import jakarta.ws.rs.DELETE;
import jakarta.ws.rs.GET;
import jakarta.ws.rs.POST;
import jakarta.ws.rs.PUT;
import jakarta.ws.rs.Path;
import jakarta.ws.rs.PathParam;
import jakarta.ws.rs.Produces;
import jakarta.ws.rs.core.MediaType;
import jakarta.ws.rs.core.Response;


@Path("/chamados")
@Produces(MediaType.APPLICATION_JSON)
@Consumes(MediaType.APPLICATION_JSON)
public class ChamadoResource {

    @Inject
    ChamadoService chamadoService;

    @GET
    public List<ChamadoDTO> list() {

        return chamadoService.listarTodos();
    }

    @GET
    @Path("/{id}")
    public ChamadoDTO get(@PathParam("id") Long id) {

        return chamadoService.buscarPorId(id);
    }

    @GET
    @Path("/status/{status}")
    public List<ChamadoDTO> getByStatus(@PathParam("status") StatusChamado status) {

        return chamadoService.buscarPorStatus(status);
    }

    @GET
    @Path("/aluno/{matricula}")
    public List<ChamadoDTO> getByAluno(@PathParam("matricula") String matricula) {

        return chamadoService.buscarPorMatriculaAluno(matricula);
    }

    @GET
    @Path("/auxilio/{nome}")
    public List<ChamadoDTO> getByAuxilio(@PathParam("nome") String nome) {

        return chamadoService.buscarPorNomeAuxilio(nome);
    }

    @POST
    public ChamadoDTO create(ChamadoDTO dto) {

        return chamadoService.create(dto);
    }

    @PUT
    @Path("/{id}")
    public ChamadoDTO update(@PathParam("id") Long id, ChamadoDTO dto) {

        return chamadoService.update(id, dto);
    }

    @PUT
    @Path("/{id}/responder")
    public ChamadoDTO responder(@PathParam("id") Long id, String resposta) {

        return chamadoService.responder(id, resposta);
    }

    @PUT 
    @Path("/{id}/fechar")
    public ChamadoDTO fechar(@PathParam("id") Long id) {

        return chamadoService.close(id);
    }

    @DELETE
    @Path("/{id}")
    public Response delete(@PathParam("id") Long id) {
        chamadoService.delete(id);

        return Response.noContent().build();
    }
}