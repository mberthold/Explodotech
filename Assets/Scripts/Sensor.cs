using UnityEngine;
using Vector3 = UnityEngine.Vector3;
using BertisUtils;
using ExplodotechUtils;
using System.Collections.Generic;

public class Sensor : MonoBehaviour
{
    // Actual Sensor
    private Rigidbody2D shipBody;
    private PolygonCollider2D polygonCollider;
    private Vector3 origin;
    private float direction = 0.0f;
    public float fov = 30f;
    public float sensorRange = 50f;  // How far can we see?
    public int scanFrequency = 30;
    public float scanInterval;
    public float scanTimer;
    public bool visualize = true;
    private SensorPassive sensorPassive;
    private List<GameObject> ObjectsInCone = new List<GameObject>(); // Objects in the cone
    public List<GameObject> DetectedObjects = new List<GameObject>(); // The Objects we can actually see!
    public List<GameObject> displayedObjects = new List<GameObject>();

    // Visualisation
    private Mesh mesh;  // Mesh for visualization
    private MeshRenderer meshRenderer;
    public int rayCount = 30; // How closely do we want to be to an actual cone as opposed to a simple triangle? Number of subcones.

    // Start is called once before the first execution of Update after the MonoBehaviour is created
    void Start()
    {
        sensorPassive = new SensorPassive();

        mesh = new Mesh();
        GetComponent<MeshFilter>().mesh = mesh;
        meshRenderer = GetComponent<MeshRenderer>();

        origin = Vector3.zero; // This works only as long as the sensor is attached to another object. All positions are relative to the parent!

        scanInterval = 1.0f / scanFrequency;

        shipBody = GetComponentInParent<Rigidbody2D>();
        polygonCollider = GetComponent<PolygonCollider2D>();

        SetDirectionRelativeToParent(0f);
    }

    // Update is called once per frame
    void Update()
    {
        sensorPassive.UpdatePosition(this.transform.position);
        DrawCone();

        if (meshRenderer != null)
        {
            meshRenderer.enabled = visualize;
        }

        scanTimer -= Time.deltaTime;
        if (scanTimer < 0)
        {
            scanTimer += scanInterval;
            Scan();
        }
    }

    public void SetOrigin(Vector3 origin)
    {
        this.origin = origin;
    }

    public void SetDirectionRelativeToParent(float direction)
    {
        /*
        * Sets the direction RELATIVE to the parent object!
        */
        this.direction = direction;
        this.direction += 90f;
        this.direction += this.fov / 2;
    }

    private void DrawCone()
    {
        float angle = this.direction;
        float angleIncrement = fov / rayCount;  // Width of each individual sub cone

        (Vector3[] vertices, Vector2[] points) = SensorUtils.CalculateCone(this.origin, this.direction, this.fov, this.rayCount, this.sensorRange);
        Vector2[] uv = new Vector2[vertices.Length];
        int[] triangles = new int[rayCount * 3];
        
        // ######################################################################
        // Define the triangles for the mesh!
        int vertexIndex = 1;
        int triangleIndex = 0;
        for (int i = 0; i <= rayCount; i++)
        {
            if (i > 0)
            {
                triangles[triangleIndex + 0] = 0;
                triangles[triangleIndex + 1] = vertexIndex - 1;
                triangles[triangleIndex + 2] = vertexIndex;
                triangleIndex += 3;
            }
            angle -= angleIncrement;
            vertexIndex++;

        }

        triangles[0] = 0;
        triangles[1] = 1;
        triangles[2] = 2;

        mesh.vertices = vertices;
        mesh.uv = uv;
        mesh.triangles = triangles;
        mesh.bounds = new Bounds(origin, Vector3.one * 1000);
        // ######################################################################

        // Set the points for the Polygon Collider
        polygonCollider.points = points;
    }

    public void Scan()
    {
        sensorPassive.ObjectsInCone = ObjectsInCone;
        sensorPassive.Scan();
        DetectedObjects = sensorPassive.DetectedObjects;

        // This part is not thought through yet!
        foreach (GameObject obj in DetectedObjects)
        {
            if (!displayedObjects.Contains(obj))
            {
                displayedObjects.Add(obj);
            }
        }

        for (int i = displayedObjects.Count - 1; i >= 0; i--)
        {
            GameObject obj = displayedObjects[i];
            if (!DetectedObjects.Contains(obj))
            {
                obj.transform.position = VectorUtils.TransformSetZ(obj, 0f);
                displayedObjects.RemoveAt(i);
            }
            else
            {
                obj.transform.position = VectorUtils.TransformSetZ(obj, 1f);
            }
        }
        
    }

    void OnTriggerEnter2D(Collider2D other)
    {
        // Add Object to the List of objects in Cone
        if (!ObjectsInCone.Contains(other.gameObject))
        {
            ObjectsInCone.Add(other.gameObject);
            Debug.Log($"Object entered cone: {other.gameObject.name}");
        }
    }

    void OnTriggerExit2D(Collider2D other)
    {
        // Remove Objects from the list of objects in the cone
        if (ObjectsInCone.Contains(other.gameObject))
        {
            ObjectsInCone.Remove(other.gameObject);
            Debug.Log($"Object exited cone: {other.gameObject.name}");
        }
    }

    void OnTriggerStay2D(Collider2D other)
    {
        //Debug.Log("Stay");   
    }

}
