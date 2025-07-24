using System.Text.Json.Serialization;
using System.ComponentModel.DataAnnotations.Schema;

public class Paint
{
    [Column("product_id")]
    public string? ProductId { get; set; }
    [Column("name")]
    public string? Name { get; set; }
    [Column("brand")]
    public string? Brand { get; set; }
    [Column("paint_type")]
    public string? PaintType { get; set; }
    [Column("grade")]
    public string? Grade { get; set; }
    [Column("hex_code")]
    public string? HexCode { get; set; }
    [Column("cielab_l")]
    public double CielabL { get; set; }
    [Column("cielab_a")]
    public double CielabA { get; set; }
    [Column("cielab_b")]
    public double CielabB { get; set; }
    [Column("is_deleted")]
    public bool IsDeleted { get; set; }
}