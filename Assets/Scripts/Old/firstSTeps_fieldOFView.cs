/*using System.Numerics;
using UnityEngine;
using UnityEngine.Rendering.Universal;
using Vector2 = UnityEngine.Vector2;
using Vector3 = UnityEngine.Vector3;
using Unity.Mathematics;

public class fieldOFView : MonoBehaviour
{
    // Start is called once before the first execution of Update after the MonoBehaviour is created
    private Mesh mesh;
    private Vector3 origin;
    private float direction = 0.0f;
    private float fov = 30f;
    float sensorRange = 50f;  // How far can we see?
    public int scanFrequency = 30;
    public LayerMask layers;
    int count;
    float scanInterval;
    float scanTimer;

    void Start()
    {
        mesh = new Mesh();
        GetComponent<MeshFilter>().mesh = mesh;
        origin = Vector3.zero;

        scanInterval = 1.0f / scanFrequency;

    }

    // Update is called once per frame
    void Update()
    {
        Debug.Log(origin);
        // Width of the sensor cone

        int rayCount = 30;  // How closely do we want to be to an actual cone as opposed to a simple triangle? Number of subcones.
        float angle = this.direction;
        float angleIncrement = fov / rayCount;  // Width of each individual sub cone


        Vector3[] vertices = new Vector3[rayCount + 1 + 1];
        Vector2[] uv = new Vector2[vertices.Length];
        int[] triangles = new int[rayCount * 3];

        vertices[0] = origin;

        int vertexIndex = 1;
        int triangleIndex = 0;
        for (int i = 0; i <= rayCount; i++)
        {
            Vector3 vertex = origin + GetVectorFromAngle(angle) * sensorRange;
            vertices[vertexIndex] = vertex;

            if (i > 0)
            {
                triangles[triangleIndex + 0] = 0;
                triangles[triangleIndex + 1] = vertexIndex - 1;
                triangles[triangleIndex + 2] = vertexIndex;
                triangleIndex += 3;
            }

            vertexIndex++;
            angle -= angleIncrement;


        }

        triangles[0] = 0;
        triangles[1] = 1;
        triangles[2] = 2;

        mesh.vertices = vertices;
        mesh.uv = uv;
        mesh.triangles = triangles;
        mesh.bounds = new Bounds(origin, Vector3.one * 1000);

        scanTimer -= Time.deltaTime;
        if (scanTimer < 0)
        {
            scanTimer += scanInterval;
            Scan();
        }

    }

    public Vector3 GetVectorFromAngle(float angle)
    {
        // Returns a vector of length 1!
        // 0 <= angle <= 360
        float angleRad = angle * (Mathf.PI / 180f);
        return new Vector3(Mathf.Cos(angleRad), Mathf.Sin(angleRad));
    }

    public void SetOrigin(Vector3 origin)
    {
        this.origin = origin;
    }

    public void SetDirection(float direction)
    {
        this.direction = direction;
        this.direction += 90f;
        this.direction += this.fov / 2;
    }

    public void Scan()
    {
        //Collider[] colliders = Physics.OverlapSphere(origin, sensorRange);
        Vector2 origin2D = origin;
        Collider2D[] colliders = new Collider2D[10];
        ContactFilter2D filter = new ContactFilter2D();
        filter.NoFilter();
        int number_of_results = Physics2D.OverlapCircle(origin2D, sensorRange, filter, colliders);
        Debug.Log(number_of_results);

    }
}
*/